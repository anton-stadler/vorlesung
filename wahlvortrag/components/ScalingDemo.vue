<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'

// ── Layout constants (SVG coordinate space 800 × 250) ─────────────────────────
const SVG_W = 800
const SVG_H = 250
const BRX = 305
const BRW = 155
const BRY = 55
const BRH = 138
const WRK_X = 548  // links genug, damit Pods die Capacity (rechts bei 768) nicht überlagern

// ── Labels ────────────────────────────────────────────────────────────────────
const VLABELS    = ['small', 'medium', 'large', 'x-large']
const VCOSTS     = [1.00, 2.00, 4.00, 8.00]
const VRATE_MULT = [1, 2, 4, 8]   // multipliers relative to baseRate
const MTITLES    = [
  'Direct Connection – Single Machine',
  'Broker + Single Machine',
  'Broker + Horizontal Scaling (Manual)',
  'Broker + Horizontal Scaling (Auto)',
]

// ── Core state ────────────────────────────────────────────────────────────────
const mode          = ref(1)
const cameras       = ref(3)
const verticalSize  = ref(1)
const manualWorkers = ref(2)
const autoWorkers   = ref([{ id: 1, status: 'active', addedAt: 0, load: 0 }])
const queueLength   = ref(0)
const messagesLost  = ref(0)
const packets       = ref([])
const cameraFiring  = reactive({})
const isBurst       = ref(false)
const canvasOpacity = ref(1)
const isRestarting  = ref(false)
const restartProgress = ref(0)

const PROCESSING_TIME_MS = 200
const DOWNTIME_MS       = 3000
const FIRE_ANIM_MS       = 800
const MAX_PACKETS        = 28
const BURST_DURATION_MS  = 5000
const BURST_RATE_FACTOR  = 3

let packetId          = 0
let workerId          = 1
let intervalId        = null
let cameraFireTimeout = null
let burstTimer        = null
let scaleUpCD         = 0
let scaleDownCD       = 0
let cameraFireStopped = false
let restartIntervalId = null
let restartTimeoutId  = null

// ── Settings ──────────────────────────────────────────────────────────────────
const settingsOpen   = ref(false)
const ratePerCamera  = ref(0.5)   // req/s per camera (default ½/s)
const baseRate       = ref(1.0)   // processing fps for small instance
const randomizer     = ref(0)     // 0 = deterministic, 1 = chaotic
const showAnimations = ref(true)  // camera flash + dashed connectors
const startupTimeMs  = ref(1000)  // Pod startup delay (ms) until status 'active'

// ── Auto-Scaling (Mode 4) ──────────────────────────────────────────────────────
const autoScaleStrategy  = ref('queue')   // 'queue' | 'load' | 'latency' | 'hybrid'
const autoScaleMenuOpen   = ref(false)
const modeMenuOpen        = ref(false)
const queueScaleUp        = ref(3)
const queueScaleDown      = ref(1)
const loadTargetPct       = ref(70)
const loadScaleUpPct      = ref(80)
const loadScaleDownPct    = ref(30)
const latencyScaleUpMs    = ref(400)
const latencyScaleDownMs  = ref(200)
// Hybrid reuses queueScaleUp/Down and latencyScaleUpMs/latencyScaleDownMs

const autoScaleStrategyLabel = computed(() => {
  const s = autoScaleStrategy.value
  if (s === 'queue') return 'Queue'
  if (s === 'load') return `Load (${loadTargetPct.value}%)`
  if (s === 'latency') return 'Latency'
  return 'Hybrid'
})

const randomizerLabel = computed(() => {
  const r = randomizer.value
  if (r < 0.01) return 'gleichmäßig'
  if (r < 0.30) return 'leicht variabel'
  if (r < 0.60) return 'variabel'
  if (r < 0.85) return 'burstig'
  return 'chaotisch'
})

// connectorDash is now per-camera (see template) — this helper is no longer used

// ── Dark mode detection ───────────────────────────────────────────────────────
const isDark = ref(false)
let darkObserver = null

// ── Color palette ─────────────────────────────────────────────────────────────
const C = computed(() => isDark.value ? {
  bg:        '#282A36',
  card:      '#383A4A',
  fg:        '#F8F8F2',
  border:    '#44475A',
  muted:     '#6272A4',
  vMuted:    '#6272A4',
  cyan:      '#8BE9FD',
  purple:    '#BD93F9',
  orange:    '#FFB86C',
  red:       '#FF5555',
  teal:      '#50FA7B',
  connector: '#44475A',
  barBg:     '#44475A',
  camLens:   '#44475A',
  flash:     '#F1FA8C',   // Dracula yellow
  flashLine: '#8BE9FD',   // bright cyan for line flash
} : {
  bg:        '#F8FAFC',
  card:      '#FFFFFF',
  fg:        '#1A2B3C',
  border:    '#E2E8F0',
  muted:     '#64748B',
  vMuted:    '#94A3B8',
  cyan:      '#028090',
  purple:    '#7B5EA7',
  orange:    '#F4A261',
  red:       '#E63946',
  teal:      '#0D9488',
  connector: '#CBD5E1',
  barBg:     '#E2E8F0',
  camLens:   '#E2E8F0',
  flash:     '#F59E0B',   // amber yellow
  flashLine: '#028090',   // teal for line flash
})

// ── Camera positions: immer in SVG-Höhe einpassen (auch bei 10 Kameras) ───────
const camPositions = computed(() => {
  const n      = cameras.value
  const margin = 24
  const range  = SVG_H - 2 * margin
  const step   = n <= 1 ? 0 : range / (n - 1)
  return Array.from({ length: n }, (_, i) => ({
    x: 76,
    y: Math.round(margin + (n <= 1 ? range / 2 : i * step))
  }))
})

// ── Ankerpunkte auf der linken Kante des Broker/Server (25 %–75 % der Höhe) ───
const camArrowTargets = computed(() => {
  const n = cameras.value
  let targetX, topY, boxH
  if (mode.value === 1) {
    const s = sBox.value
    targetX = s.x; topY = s.y; boxH = s.h
  } else {
    targetX = BRX; topY = BRY; boxH = BRH
  }
  return Array.from({ length: n }, (_, i) => {
    const t = n <= 1 ? 0.5 : 0.25 + (i / (n - 1)) * 0.5
    return { x: targetX, y: Math.round(topY + boxH * t) }
  })
})

// ── Worker grid (kompakte Pod-Höhe, damit bis zu 16 Pods passen) ──────────────
const WRK_CAPACITY_X = 768  // Capacity-Label rechts der Pods (wie Requests links der Kameras)
// Pod-Inhalt linksbündig mit Abstand, damit „Pod 16“ / „starting…“ nicht abgeschnitten wird
const POD_LEFT_PAD = 10
const POD_ICON_W = 4
const POD_GAP = 5
function workerGrid(count) {
  const cols = 2, bW = 80, bH = 26, gX = 6, gY = 4
  const rows = Math.ceil(count / cols)
  const totH = rows * bH + (rows - 1) * gY
  const sy   = Math.max(12, Math.round((SVG_H - totH) / 2))
  return Array.from({ length: count }, (_, i) => ({
    x: WRK_X + (i % cols) * (bW + gX),
    y: sy + Math.floor(i / cols) * (bH + gY),
    w: bW, h: bH,
  }))
}

const mode3Positions = computed(() => workerGrid(manualWorkers.value))
const mode4Positions = computed(() => workerGrid(autoWorkers.value.length))

// ── Server box ────────────────────────────────────────────────────────────────
const sBox = computed(() => {
  const s = [{ w: 96, h: 62 }, { w: 115, h: 80 }, { w: 140, h: 100 }, { w: 170, h: 128 }][verticalSize.value - 1]
  return { x: WRK_X, y: Math.round((SVG_H - s.h) / 2), ...s }
})

// ── Metrics ───────────────────────────────────────────────────────────────────
const incomingRate = computed(() => {
  const mult = isBurst.value ? BURST_RATE_FACTOR : 1
  return cameras.value * ratePerCamera.value * mult
})

const processingRate = computed(() => {
  if (mode.value <= 2 && isRestarting.value) return 0
  if (mode.value <= 2) return baseRate.value * VRATE_MULT[verticalSize.value - 1]
  if (mode.value === 3) return manualWorkers.value * baseRate.value
  return Math.max(autoWorkers.value.filter(w => w.status === 'active').length, 1) * baseRate.value
})

const throughput    = computed(() => Math.round(Math.min(processingRate.value, incomingRate.value)))
const isOverloaded  = computed(() => mode.value === 1 && incomingRate.value > processingRate.value)
const costPerHour   = computed(() => {
  if (mode.value <= 2) return VCOSTS[verticalSize.value - 1]
  if (mode.value === 3) return manualWorkers.value * 0.5
  return Math.max(autoWorkers.value.filter(w => w.status === 'active').length, 1) * 0.5
})

const workerUtilPct = computed(() => {
  const cap = processingRate.value
  return cap <= 0 ? 0 : Math.min(1, incomingRate.value / cap)
})

const effectiveLoad = computed(() =>
  queueLength.value >= 20 ? 1 : workerUtilPct.value
)

const latencyMs = computed(() => {
  const rate = processingRate.value
  if (rate <= 0) return null
  if (mode.value === 1) return PROCESSING_TIME_MS  // Keine Queue → nur Bearbeitungszeit
  return Math.round((queueLength.value / rate) * 1000 + PROCESSING_TIME_MS)
})

const queueBarW  = computed(() => Math.round((Math.min(queueLength.value, 20) / 20) * (BRW - 22)))
const queueColor = computed(() =>
  queueLength.value >= 8 ? C.value.red :
  queueLength.value >= 5 ? C.value.orange :
  C.value.cyan
)

// ── Camera fire delay (with randomizer) ───────────────────────────────────────
function getFireDelay() {
  const mult = isBurst.value ? BURST_RATE_FACTOR : 1
  const base = 1000 / Math.max(0.1, cameras.value * ratePerCamera.value * mult)
  const r = randomizer.value
  if (r < 0.001) return base
  const noise = (Math.random() * 2 - 1) * r * 2
  return Math.max(50, base * (1 + noise))
}

// ── Packets ───────────────────────────────────────────────────────────────────
function spawnPacket(x1, y1, x2, y2, color, ms) {
  if (packets.value.length >= MAX_PACKETS) return
  const id = ++packetId
  packets.value.push({ id, x1, y1, x2, y2, color, ms })
  setTimeout(() => {
    const i = packets.value.findIndex(p => p.id === id)
    if (i !== -1) packets.value.splice(i, 1)
  }, ms + 120)
}

function fireOneCamera() {
  try {
    const n = cameras.value
    if (n < 1) return
    if (showAnimations.value) {
      const idx = Math.floor(Math.random() * n)
      cameraFiring[idx] = true
      setTimeout(() => { cameraFiring[idx] = false }, FIRE_ANIM_MS)
    }
    const wouldBe = queueLength.value + 1
    const newQueue = Math.min(20, wouldBe)
    const lost = wouldBe - newQueue
    const countAsLost = lost > 0 && (mode.value !== 1 || incomingRate.value > processingRate.value)
    if (countAsLost) messagesLost.value = messagesLost.value + lost
    queueLength.value = newQueue
  } finally {
    if (!cameraFireStopped) {
      cameraFireTimeout = setTimeout(fireOneCamera, getFireDelay())
    }
  }
}

function spawnBrokerPackets() {
  if (mode.value === 1 || queueLength.value <= 0) return
  const ppt = processingRate.value * 0.2
  const n   = Math.floor(ppt) + (Math.random() < ppt % 1 ? 1 : 0)
  let targets = []
  if (mode.value === 2) {
    const s = sBox.value; targets = [{ x: s.x, y: s.y + s.h / 2 }]
  } else if (mode.value === 3) {
    targets = mode3Positions.value.map(wp => ({ x: wp.x, y: wp.y + wp.h / 2 }))
  } else {
    const actives = autoWorkers.value.filter(w => w.status === 'active')
    const pos = mode4Positions.value
    targets = actives.map((_, i) => pos[i] ? { x: pos[i].x, y: pos[i].y + pos[i].h / 2 } : null).filter(Boolean)
  }
  if (!targets.length) return
  for (let i = 0; i < n; i++) {
    if (packets.value.length >= MAX_PACKETS) break
    const t = targets[Math.floor(Math.random() * targets.length)]
    spawnPacket(BRX + BRW, BRY + BRH / 2, t.x, t.y, C.value.orange, 780)
  }
}

// ── KEDA / Auto-Scale ─────────────────────────────────────────────────────────
function runKEDA() {
  const now = Date.now()
  const q = queueLength.value
  const load = effectiveLoad.value
  const lat = latencyMs.value
  const strategy = autoScaleStrategy.value
  const activeCount = autoWorkers.value.filter(w => w.status === 'active').length

  autoWorkers.value.forEach(w => {
    if (w.status === 'starting' && now - w.addedAt >= startupTimeMs.value) w.status = 'active'
  })
  autoWorkers.value = autoWorkers.value.filter(w =>
    !(w.status === 'stopping' && now - w.stoppedAt >= 400)
  )
  const nonStopping = autoWorkers.value.filter(w => w.status !== 'stopping').length

  let shouldScaleUp = false
  let shouldScaleDown = false

  if (strategy === 'queue') {
    shouldScaleUp = q > queueScaleUp.value
    shouldScaleDown = q < queueScaleDown.value
  } else if (strategy === 'load') {
    shouldScaleUp = load > loadScaleUpPct.value / 100
    shouldScaleDown = load < loadScaleDownPct.value / 100
  } else if (strategy === 'latency') {
    shouldScaleUp = lat != null && lat > latencyScaleUpMs.value
    shouldScaleDown = lat != null && lat < latencyScaleDownMs.value
  } else if (strategy === 'hybrid') {
    shouldScaleUp = q > queueScaleUp.value || (lat != null && lat > latencyScaleUpMs.value)
    shouldScaleDown = q < queueScaleDown.value && (lat == null || lat < latencyScaleDownMs.value)
  }

  if (shouldScaleUp && nonStopping < 16 && scaleUpCD <= 0) {
    autoWorkers.value.push({ id: ++workerId, status: 'starting', addedAt: now, load: 0 })
    scaleUpCD = 12
  }
  if (shouldScaleDown && activeCount > 1 && scaleDownCD <= 0) {
    const last = [...autoWorkers.value].reverse().find(w => w.status === 'active')
    if (last) { last.status = 'stopping'; last.stoppedAt = now; scaleDownCD = 25 }
  }
  if (scaleUpCD > 0) scaleUpCD--
  if (scaleDownCD > 0) scaleDownCD--
}

// ── Tick ──────────────────────────────────────────────────────────────────────
function tick() {
  const proc    = processingRate.value * 0.2
  const wouldBe = queueLength.value - proc
  queueLength.value = Math.max(0, Math.min(20, wouldBe))
  if (mode.value === 4) runKEDA()
  spawnBrokerPackets()
}

// ── Mode switch ───────────────────────────────────────────────────────────────
function switchMode(m) {
  if (m === mode.value) return
  canvasOpacity.value = 0
  setTimeout(() => {
    mode.value = m; queueLength.value = 0; messagesLost.value = 0; packets.value = []
    Object.keys(cameraFiring).forEach(k => delete cameraFiring[k])
    if (m === 4) {
      autoWorkers.value = [{ id: ++workerId, status: 'active', addedAt: Date.now(), load: 0 }]
      scaleUpCD = scaleDownCD = 0
    }
    canvasOpacity.value = 1
  }, 200)
}

function fireBurst() {
  if (isBurst.value) {
    if (burstTimer) clearTimeout(burstTimer)
    burstTimer = null
    isBurst.value = false
    return
  }
  isBurst.value = true
  burstTimer = setTimeout(() => { isBurst.value = false; burstTimer = null }, BURST_DURATION_MS)
}

// ── Downtime bei vertikaler Skalierung (Modus 1 & 2) ─────────────────────────────
watch(verticalSize, (newVal, oldVal) => {
  if (mode.value > 2) return
  if (oldVal === undefined) return // initial mount, skip
  if (restartIntervalId) clearInterval(restartIntervalId)
  if (restartTimeoutId) clearTimeout(restartTimeoutId)
  isRestarting.value = true
  restartProgress.value = 0
  const stepMs = 100
  const steps = DOWNTIME_MS / stepMs
  let step = 0
  restartIntervalId = setInterval(() => {
    step += 1
    restartProgress.value = Math.min(1, step / steps)
    if (step >= steps) {
      clearInterval(restartIntervalId)
      restartIntervalId = null
      isRestarting.value = false
      restartProgress.value = 0
    }
  }, stepMs)
  restartTimeoutId = setTimeout(() => {
    if (restartIntervalId) clearInterval(restartIntervalId)
    restartIntervalId = null
    restartTimeoutId = null
    isRestarting.value = false
    restartProgress.value = 0
  }, DOWNTIME_MS)
})

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
  darkObserver = new MutationObserver(() => {
    isDark.value = document.documentElement.classList.contains('dark')
  })
  darkObserver.observe(document.documentElement, { attributeFilter: ['class'] })

  cameraFireStopped = false
  intervalId = setInterval(tick, 200)
  cameraFireTimeout = setTimeout(fireOneCamera, getFireDelay())
})

onUnmounted(() => {
  darkObserver?.disconnect()
  cameraFireStopped = true
  clearInterval(intervalId)
  if (cameraFireTimeout) clearTimeout(cameraFireTimeout)
  if (burstTimer)        clearTimeout(burstTimer)
  if (restartIntervalId) clearInterval(restartIntervalId)
  if (restartTimeoutId)  clearTimeout(restartTimeoutId)
})
</script>

<template>
  <div class="sd" :class="{ 'sd--dark': isDark }">

    <!-- Controls -->
    <div class="sd-ctrl">
      <div class="mode-dropdown-wrap">
        <button
          type="button"
          class="mode-dropdown-btn"
          :class="{ active: modeMenuOpen }"
          @click="modeMenuOpen = !modeMenuOpen"
          :title="MTITLES[mode - 1]">
          {{ MTITLES[mode - 1] }}
        </button>
        <Transition name="spanel">
          <div v-if="modeMenuOpen" class="mode-dropdown-panel">
            <button
              v-for="(title, i) in MTITLES"
              :key="i"
              type="button"
              class="mode-option"
              :class="{ active: mode === i + 1 }"
              @click="switchMode(i + 1); modeMenuOpen = false">
              {{ title }}
            </button>
          </div>
        </Transition>
      </div>

      <div class="sliders-row">
        <label class="sl">
          Cameras <strong>{{ cameras }}</strong>
          <input type="range" min="1" max="10" v-model.number="cameras" />
        </label>
        <label v-if="mode <= 2" class="sl">
          Server <strong class="sl-fixed">{{ VLABELS[verticalSize - 1] }}</strong>
          <input type="range" min="1" max="4" v-model.number="verticalSize" />
        </label>
        <label v-if="mode === 3" class="sl">
          Workers <strong>{{ manualWorkers }}</strong>
          <input type="range" min="1" max="16" v-model.number="manualWorkers" />
        </label>
        <button class="burst-btn" :class="{ 'burst-btn--active': isBurst }" @click="fireBurst">
          {{ isBurst ? '🔥 Bursting… (Klick zum Beenden)' : '🔥 Fire burst' }}
        </button>

        <!-- Auto-Scaling menu (Mode 4 only) -->
        <div v-if="mode === 4" class="autoscale-wrap">
          <button
            class="autoscale-btn"
            :class="{ active: autoScaleMenuOpen }"
            @click="autoScaleMenuOpen = !autoScaleMenuOpen"
            title="Auto-Scaling">📈 Auto-Scale<span class="autoscale-label">: {{ autoScaleStrategyLabel }}</span></button>
          <Transition name="spanel">
            <div v-if="autoScaleMenuOpen" class="autoscale-panel">
              <div class="sp-title">
                Auto-Scaling
                <button class="sp-close" @click="autoScaleMenuOpen = false">×</button>
              </div>
              <div class="autoscale-strategy-pills">
                <button
                  v-for="opt in ['queue', 'load', 'latency', 'hybrid']"
                  :key="opt"
                  class="mpill"
                  :class="{ active: autoScaleStrategy === opt }"
                  @click="autoScaleStrategy = opt">
                  {{ opt === 'queue' ? 'Queue' : opt === 'load' ? 'Load' : opt === 'latency' ? 'Latency' : 'Hybrid' }}
                </button>
              </div>
              <p v-if="autoScaleStrategy === 'queue'" class="autoscale-hint">Skaliert nach Nachrichten in der Queue.</p>
              <p v-else-if="autoScaleStrategy === 'load'" class="autoscale-hint">Skaliert nach durchschnittlicher Auslastung (Ziel).</p>
              <p v-else-if="autoScaleStrategy === 'latency'" class="autoscale-hint">Skaliert nach Latenz (Wartezeit in der Queue).</p>
              <p v-else class="autoscale-hint">Scale-up wenn Queue ODER Latenz Schwellen überschreiten.</p>
              <div class="sp-sep"></div>
              <!-- Queue thresholds -->
              <template v-if="autoScaleStrategy === 'queue' || autoScaleStrategy === 'hybrid'">
                <div class="sp-row">
                  <span class="sp-label">Scale-up ab Queue</span>
                  <input type="range" min="1" max="10" v-model.number="queueScaleUp" class="sp-slider" />
                  <span class="sp-val">{{ queueScaleUp }}</span>
                </div>
                <div class="sp-row">
                  <span class="sp-label">Scale-down unter Queue</span>
                  <input type="range" min="0" max="5" v-model.number="queueScaleDown" class="sp-slider" />
                  <span class="sp-val">{{ queueScaleDown }}</span>
                </div>
                <div v-if="autoScaleStrategy === 'hybrid'" class="sp-sep"></div>
              </template>
              <!-- Load thresholds -->
              <template v-if="autoScaleStrategy === 'load'">
                <div class="sp-row">
                  <span class="sp-label">Ziel Load</span>
                  <input type="range" min="40" max="95" v-model.number="loadTargetPct" class="sp-slider" />
                  <span class="sp-val">{{ loadTargetPct }}%</span>
                </div>
                <div class="sp-row">
                  <span class="sp-label">Scale-up ab</span>
                  <input type="range" min="50" max="98" v-model.number="loadScaleUpPct" class="sp-slider" />
                  <span class="sp-val">{{ loadScaleUpPct }}%</span>
                </div>
                <div class="sp-row">
                  <span class="sp-label">Scale-down unter</span>
                  <input type="range" min="5" max="50" v-model.number="loadScaleDownPct" class="sp-slider" />
                  <span class="sp-val">{{ loadScaleDownPct }}%</span>
                </div>
              </template>
              <!-- Latency thresholds (also for hybrid) -->
              <template v-if="autoScaleStrategy === 'latency' || autoScaleStrategy === 'hybrid'">
                <div class="sp-row">
                  <span class="sp-label">Scale-up ab Latency</span>
                  <input type="range" min="200" max="800" step="50" v-model.number="latencyScaleUpMs" class="sp-slider" />
                  <span class="sp-val">{{ latencyScaleUpMs }} ms</span>
                </div>
                <div class="sp-row">
                  <span class="sp-label">Scale-down unter Latency</span>
                  <input type="range" min="100" max="400" step="50" v-model.number="latencyScaleDownMs" class="sp-slider" />
                  <span class="sp-val">{{ latencyScaleDownMs }} ms</span>
                </div>
              </template>
            </div>
          </Transition>
        </div>
      </div>

      <!-- Settings gear -->
      <div class="settings-wrap">
        <button
          class="settings-btn"
          :class="{ active: settingsOpen }"
          @click="settingsOpen = !settingsOpen"
          title="Einstellungen">⚙</button>

        <Transition name="spanel">
          <div v-if="settingsOpen" class="settings-panel">
            <div class="sp-title">
              Einstellungen
              <button class="sp-close" @click="settingsOpen = false">×</button>
            </div>

            <div class="sp-row">
              <span class="sp-label">Req / Kamera</span>
              <input type="range" min="0.1" max="2" step="0.1"
                     v-model.number="ratePerCamera" class="sp-slider" />
              <span class="sp-val">{{ ratePerCamera.toFixed(1) }}/s</span>
            </div>

            <div class="sp-row">
              <span class="sp-label">Rate / Instanz <span class="sp-sub">(small)</span></span>
              <input type="range" min="0.5" max="6" step="0.5"
                     v-model.number="baseRate" class="sp-slider" />
              <span class="sp-val">{{ baseRate.toFixed(1) }}/s</span>
            </div>

            <div class="sp-row">
              <span class="sp-label">Startup-Time</span>
              <input type="range" min="500" max="8000" step="500"
                     v-model.number="startupTimeMs" class="sp-slider" />
              <span class="sp-val">{{ (startupTimeMs / 1000).toFixed(1) }} s</span>
            </div>

            <div class="sp-sep"></div>

            <div class="sp-row">
              <span class="sp-label">Randomizer</span>
              <input type="range" min="0" max="1" step="0.05"
                     v-model.number="randomizer" class="sp-slider" />
              <span class="sp-val sp-rand-label">{{ randomizerLabel }}</span>
            </div>

            <div class="sp-sep"></div>

            <div class="sp-row sp-row-toggle">
              <span class="sp-label">Animationen</span>
              <label class="sp-toggle">
                <input type="checkbox" v-model="showAnimations" />
                <span class="sp-toggle-track" :class="{ on: showAnimations }">
                  <span class="sp-toggle-thumb"></span>
                </span>
                <span class="sp-toggle-lbl">{{ showAnimations ? 'an' : 'aus' }}</span>
              </label>
            </div>
          </div>
        </Transition>
      </div>
    </div>

    <!-- SVG Canvas -->
    <div class="sd-canvas" :style="{ opacity: canvasOpacity, transition: 'opacity 0.2s' }">
      <svg :width="SVG_W" :height="SVG_H" :viewBox="`0 0 ${SVG_W} ${SVG_H}`"
           xmlns="http://www.w3.org/2000/svg"
           style="width:100%;display:block;font-family:'JetBrains Mono',monospace;">

        <!-- Background -->
        <rect class="sd-canvas-bg" width="800" height="250" rx="6" />

        <!-- Pfeilspitzen-Marker -->
        <defs>
          <marker id="arr" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto">
            <path d="M0,0.5 L0,6.5 L6.5,3.5 z" :fill="C.vMuted" />
          </marker>
        </defs>

        <!-- Connector lines: cameras → Broker/Server, verteilt 25 %–75 %, Pfeilspitze, aktiv = durchgezogen -->
        <line v-for="(cam, i) in camPositions" :key="`cl-${i}`"
          :x1="cam.x + 5" :y1="cam.y"
          :x2="camArrowTargets[i].x" :y2="camArrowTargets[i].y"
          :stroke="showAnimations && cameraFiring[i] ? C.flashLine : C.connector"
          stroke-width="1"
          :stroke-dasharray="showAnimations && cameraFiring[i] ? 'none' : '4 3'"
          marker-end="url(#arr)" />

        <!-- Connector: broker → server (Mode 2) — always dashed -->
        <line v-if="mode === 2"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="sBox.x" :y2="sBox.y + sBox.h / 2"
          :stroke="C.connector" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Connectors: broker → workers (Mode 3) — always dashed -->
        <line v-if="mode === 3" v-for="(wp, i) in mode3Positions" :key="`wl3-${i}`"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="wp.x" :y2="wp.y + wp.h / 2"
          :stroke="C.connector" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Connectors: broker → auto-workers (Mode 4) — always dashed -->
        <line v-if="mode === 4" v-for="(wp, i) in mode4Positions" :key="`wl4-${i}`"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="wp.x" :y2="wp.y + wp.h / 2"
          :stroke="C.connector" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Left: Requests -->
        <g>
          <text x="22" y="118" text-anchor="middle" :fill="C.muted" style="font-size:9px;font-weight:bold">Requests</text>
          <text x="22" y="132" text-anchor="middle" :fill="C.cyan" style="font-size:11px;font-weight:bold">{{ incomingRate.toFixed(1) }}</text>
          <text x="22" y="144" text-anchor="middle" :fill="C.vMuted" style="font-size:8px">req/s</text>
        </g>

        <!-- Right: Capacity (in allen Modi) -->
        <g>
          <text :x="WRK_CAPACITY_X" y="118" text-anchor="middle" :fill="C.muted" style="font-size:9px;font-weight:bold">Capacity</text>
          <text :x="WRK_CAPACITY_X" y="132" text-anchor="middle" :fill="C.purple" style="font-size:11px;font-weight:bold">{{ processingRate.toFixed(1) }}</text>
          <text :x="WRK_CAPACITY_X" y="144" text-anchor="middle" :fill="C.vMuted" style="font-size:8px">req/s</text>
        </g>

        <!-- CAMERAS -->
        <g v-for="(cam, i) in camPositions" :key="`cam-${i}`">
          <text :x="cam.x + 14" :y="cam.y + 4" style="font-size:14px"
                :fill="C.flash"
                class="cam-flash" :class="{ firing: showAnimations && cameraFiring[i] }">⚡</text>
          <rect :x="cam.x - 12" :y="cam.y - 8" width="16" height="12" rx="2" :fill="C.cyan" />
          <circle :cx="cam.x - 4" :cy="cam.y - 2" r="4"   :fill="C.camLens" />
          <circle :cx="cam.x - 4" :cy="cam.y - 2" r="2.5" :fill="C.cyan" />
          <rect :x="cam.x - 10" :y="cam.y - 13" width="5" height="4" rx="1" :fill="C.cyan" />
        </g>

        <!-- BROKER (Modes 2, 3, 4) -->
        <g v-if="mode > 1">
          <rect :x="BRX" :y="BRY" :width="BRW" :height="BRH"
                rx="7" :fill="C.card" :stroke="C.orange" stroke-width="2" />
          <text :x="BRX + 18" :y="BRY + 20" style="font-size:14px">📮</text>
          <text :x="BRX + 36" :y="BRY + 21" :fill="C.fg" font-weight="bold"
                style="font-size:11px">Message Broker</text>
          <text :x="BRX + 11" :y="BRY + 38" :fill="C.muted"
                style="font-size:9px">Queue: {{ Math.round(queueLength) }} / 20</text>
          <rect :x="BRX + 11" :y="BRY + 43" :width="BRW - 22" height="9" rx="4" :fill="C.barBg" />
          <rect :x="BRX + 11" :y="BRY + 43" :width="queueBarW" height="9" rx="4" :fill="queueColor" />
          <line :x1="BRX + 11 + (5/20)*(BRW-22)" :y1="BRY + 42"
                :x2="BRX + 11 + (5/20)*(BRW-22)" :y2="BRY + 53"
                :stroke="C.orange" stroke-width="1.5" opacity="0.8" />
          <line :x1="BRX + 11 + (8/20)*(BRW-22)" :y1="BRY + 42"
                :x2="BRX + 11 + (8/20)*(BRW-22)" :y2="BRY + 53"
                :stroke="C.red" stroke-width="1.5" opacity="0.8" />
          <text :x="BRX + 11"       :y="BRY + 63" :fill="C.vMuted" style="font-size:7.5px">0</text>
          <text :x="BRX + BRW - 11" :y="BRY + 63" text-anchor="end" :fill="C.vMuted" style="font-size:7.5px">20</text>
          <line :x1="BRX + 8" :y1="BRY + 72" :x2="BRX + BRW - 8" :y2="BRY + 72"
                :stroke="C.border" stroke-width="1" />
          <text :x="BRX + 11"       :y="BRY + 83" :fill="C.vMuted" style="font-size:7.5px">Incoming rate</text>
          <text :x="BRX + BRW - 11" :y="BRY + 83" text-anchor="end" :fill="C.cyan" font-weight="bold"
                style="font-size:8px">{{ incomingRate.toFixed(1) }} fps</text>
          <text :x="BRX + 11"       :y="BRY + 96" :fill="C.vMuted" style="font-size:7.5px">Processing rate</text>
          <text :x="BRX + BRW - 11" :y="BRY + 96" text-anchor="end" :fill="C.purple" font-weight="bold"
                style="font-size:8px">{{ processingRate.toFixed(1) }} fps</text>
          <text :x="BRX + BRW / 2" :y="BRY + BRH - 10" text-anchor="middle" :fill="C.vMuted"
                style="font-size:7.5px;font-style:italic">MQTT / RabbitMQ</text>
          <text :x="BRX + BRW / 2" :y="BRY + BRH + 18" text-anchor="middle" :fill="C.muted"
                style="font-size:8px">Throughput</text>
          <text :x="BRX + BRW / 2" :y="BRY + BRH + 32" text-anchor="middle" :fill="C.teal"
                style="font-size:11px;font-weight:bold">{{ throughput }} req/s</text>
        </g>

        <!-- Throughput (Mode 1: no broker) -->
        <g v-if="mode === 1">
          <text :x="(76 + sBox.x + sBox.w/2) / 2" :y="SVG_H - 28" text-anchor="middle" :fill="C.muted"
                style="font-size:8px">Throughput</text>
          <text :x="(76 + sBox.x + sBox.w/2) / 2" :y="SVG_H - 14" text-anchor="middle" :fill="C.teal"
                style="font-size:11px;font-weight:bold">{{ throughput }} req/s</text>
        </g>

        <!-- SERVER (Modes 1 & 2) -->
        <g v-if="mode <= 2" :style="{ opacity: isRestarting ? 0.7 : 1, transition: 'opacity 0.3s' }">
          <rect v-if="isRestarting"
                :x="sBox.x - 5" :y="sBox.y - 5" :width="sBox.w + 10" :height="sBox.h + 10"
                rx="11" :fill="C.orange" class="restarting-glow" />
          <rect v-if="isOverloaded && !isRestarting"
                :x="sBox.x - 5" :y="sBox.y - 5" :width="sBox.w + 10" :height="sBox.h + 10"
                rx="11" :fill="C.red" class="overload-glow" />
          <rect :x="sBox.x" :y="sBox.y" :width="sBox.w" :height="sBox.h"
                rx="7" :fill="C.card"
                :stroke="isRestarting ? C.orange : isOverloaded ? C.red : C.border"
                :stroke-width="isRestarting || isOverloaded ? 2.5 : 1.5" />
          <g v-if="isRestarting">
            <rect :x="sBox.x + sBox.w/2 - 42" :y="sBox.y - 19" width="84" height="16" rx="8" :fill="C.orange" />
            <text :x="sBox.x + sBox.w/2" :y="sBox.y - 7"
                  text-anchor="middle" fill="white" font-weight="bold"
                  style="font-size:8px">⏳ RESTARTING…</text>
          </g>
          <g v-else-if="isOverloaded">
            <rect :x="sBox.x + sBox.w/2 - 33" :y="sBox.y - 19" width="66" height="16" rx="8" :fill="C.red" />
            <text :x="sBox.x + sBox.w/2" :y="sBox.y - 7"
                  text-anchor="middle" fill="white" font-weight="bold"
                  style="font-size:8px">OVERLOADED</text>
          </g>
          <template v-if="isRestarting">
            <rect :x="sBox.x + 7" :y="sBox.y + sBox.h - 14" :width="sBox.w - 14" height="6" rx="3" :fill="C.barBg" />
            <rect :x="sBox.x + 7" :y="sBox.y + sBox.h - 14" :width="Math.max(0, (sBox.w - 14) * restartProgress)" height="6" rx="3" :fill="C.orange" />
          </template>
          <text :x="sBox.x + sBox.w/2" :y="sBox.y + sBox.h/2 - 8"
                text-anchor="middle" style="font-size:18px">{{ isRestarting ? '⏳' : '🖥' }}</text>
          <text :x="sBox.x + sBox.w/2" :y="sBox.y + sBox.h/2 + 14"
                text-anchor="middle" :fill="C.fg" font-weight="bold"
                style="font-size:11px">{{ VLABELS[verticalSize - 1] }}</text>
        </g>

        <!-- WORKERS (Mode 3) -->
        <g v-if="mode === 3">
          <g v-for="(wp, i) in mode3Positions" :key="`w3-${i}`">
            <rect :x="wp.x" :y="wp.y" :width="wp.w" :height="wp.h"
                  rx="5" :fill="C.card" :stroke="C.purple" stroke-width="1.5" />
            <g :transform="`translate(${wp.x + POD_LEFT_PAD}, ${wp.y + wp.h/2})`">
              <text x="0" y="0" text-anchor="middle" dominant-baseline="middle"
                    class="pod-icon">⚙</text>
              <text :x="POD_ICON_W + POD_GAP" y="0" text-anchor="start" dominant-baseline="middle"
                    :fill="C.fg" class="pod-label">Pod {{ i + 1 }}</text>
            </g>
          </g>
        </g>

        <!-- AUTO-SCALE WORKERS (Mode 4) -->
        <g v-if="mode === 4">
          <g v-for="(w, i) in autoWorkers" :key="w.id"
             :style="{ opacity: w.status === 'stopping' ? 0 : w.status === 'starting' ? 0.55 : 1,
                       transition: 'opacity 0.4s ease' }">
            <template v-if="mode4Positions[i]">
              <rect :x="mode4Positions[i].x" :y="mode4Positions[i].y"
                    :width="mode4Positions[i].w" :height="mode4Positions[i].h"
                    rx="5" :fill="C.card"
                    :stroke="w.status === 'starting' ? C.orange : C.purple"
                    stroke-width="1.5" />
              <g :transform="`translate(${mode4Positions[i].x + POD_LEFT_PAD}, ${mode4Positions[i].y + mode4Positions[i].h/2})`">
                <text x="0" y="0" text-anchor="middle" dominant-baseline="middle"
                      class="pod-icon">{{ w.status === 'starting' ? '⏳' : '⚙' }}</text>
                <text :x="POD_ICON_W + POD_GAP" y="0" text-anchor="start" dominant-baseline="middle"
                      :fill="C.fg" :class="['pod-label', w.status === 'starting' && 'pod-label--starting']">
                  {{ w.status === 'starting' ? 'starting…' : `Pod ${i + 1}` }}
                </text>
              </g>
            </template>
          </g>
        </g>

      </svg>
    </div>

    <!-- Metrics -->
    <div class="sd-metrics">
      <div v-if="mode > 1" class="metric">
        <div class="m-label">Queue</div>
        <div class="m-val" :style="{ color: queueLength >= 8 ? C.red : queueLength >= 5 ? C.orange : undefined }">
          {{ Math.round(queueLength) }}<span class="m-unit"> / 20</span>
        </div>
      </div>
      <div class="metric">
        <div class="m-label">Load</div>
        <div class="m-val" :style="{ color: effectiveLoad >= 0.9 ? C.red : effectiveLoad >= 0.6 ? C.orange : undefined }">
          {{ Math.round(effectiveLoad * 100) }}<span class="m-unit">%</span>
        </div>
      </div>
      <div class="metric">
        <div class="m-label">Latency</div>
        <div class="m-val">
          <template v-if="latencyMs != null">≈ {{ latencyMs }}<span class="m-unit"> ms</span></template>
          <template v-else>—</template>
        </div>
      </div>
      <div class="metric" :class="{ 'metric-lost': messagesLost > 0 }">
        <div class="m-label">Messages lost</div>
        <div class="m-val" :style="{ color: messagesLost > 0 ? C.red : undefined }">{{ Math.round(messagesLost) }}</div>
      </div>
      <div class="metric">
        <div class="m-label">Cost / hr</div>
        <div class="m-val">${{ costPerHour.toFixed(2) }}</div>
        <div class="m-note">fictional</div>
      </div>
    </div>

  </div>
</template>

<style scoped>
/* ── SVG: Nur Root auf 1px (Pod-Texte haben eigene font-size) ─────────────────── */
.sd-canvas :deep(svg) { font-size: 1px !important; }
.sd-canvas :deep(.pod-icon) { font-size: 16px !important; }
.sd-canvas :deep(.pod-label) { font-size: 14px !important; font-weight: bold; }
.sd-canvas :deep(.pod-label--starting) { font-size: 10px !important; }

/* ── Container ───────────────────────────────────────────────────────────────── */
.sd {
  font-family: 'JetBrains Mono', 'Consolas', monospace;
  background: var(--slide-bg, #F8FAFC);
  border: 1px solid var(--slide-border, #E2E8F0);
  border-radius: 8px;
  padding: 9px 12px 7px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  height: 100%;
  min-height: 340px;
  box-sizing: border-box;
}

/* ── Controls row ────────────────────────────────────────────────────────────── */
.sd-ctrl {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
/* ── Mode dropdown (design-integrated, like Auto-Scale panel) ───────────────── */
.mode-dropdown-wrap {
  position: relative;
  flex-shrink: 0;
}
.mode-dropdown-btn {
  background: var(--slide-bg-card, white);
  border: 1.5px solid var(--slide-border, #CBD5E1);
  border-radius: 6px;
  padding: 6px 12px;
  font-size: 11px;
  font-family: inherit;
  cursor: pointer;
  color: var(--slide-fg, #1A2B3C);
  transition: border-color 0.18s, color 0.18s;
  width: 265px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.mode-dropdown-btn:hover,
.mode-dropdown-btn.active {
  border-color: var(--accent-cyan, #028090);
  color: var(--accent-cyan, #028090);
}
.mode-dropdown-panel {
  position: absolute;
  left: 0;
  top: calc(100% + 5px);
  z-index: 30;
  background: var(--slide-bg-card, #ffffff);
  border: 1px solid var(--slide-border, #E2E8F0);
  border-radius: 8px;
  padding: 6px 0;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.14);
  min-width: 260px;
  font-size: 10px;
}
.mode-option {
  display: block;
  width: 100%;
  padding: 8px 12px;
  border: none;
  border-radius: 0;
  background: transparent;
  color: var(--slide-fg, #1A2B3C);
  font-family: inherit;
  font-size: 11px;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.mode-option:hover {
  background: var(--slide-border, #E2E8F0);
  color: var(--slide-fg, #1A2B3C);
}
.mode-option.active {
  background: var(--accent-cyan, #028090);
  color: white;
}
.mode-option.active:hover {
  background: var(--accent-cyan, #028090);
  color: white;
}
/* Dark mode: cyan on white is hard to read → dark background + cyan text */
.sd--dark .mode-option.active {
  background: var(--slide-bg-card, #383A4A);
  color: var(--accent-cyan, #8BE9FD);
  border-left: 3px solid var(--accent-cyan, #8BE9FD);
  padding-left: 9px; /* 12px - 3px border so text aligns with others */
}
.sd--dark .mode-option.active:hover {
  background: var(--slide-bg-card, #383A4A);
  color: var(--accent-cyan, #8BE9FD);
}

.sliders-row { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
.sl { display: flex; align-items: center; gap: 5px; font-size: 10.5px; color: var(--slide-muted, #64748B); }
.sl strong { color: var(--slide-fg, #1A2B3C); }
.sl .sl-fixed { display: inline-block; min-width: 52px; text-align: left; white-space: nowrap; }
.sl input[type=range] { width: 80px; accent-color: var(--accent-cyan, #028090); cursor: pointer; }

.burst-btn {
  padding: 3px 11px;
  border-radius: 6px;
  border: 1px solid var(--slide-border, #E2E8F0);
  background: var(--slide-bg-card, #fff);
  color: var(--slide-muted, #64748B);
  font-family: inherit; font-size: 11px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, border-color 0.2s;
}
.burst-btn:hover { border-color: var(--accent-cyan, #028090); color: var(--accent-cyan, #028090); }
.burst-btn--active {
  border: none;
  background: var(--accent-red, #E63946);
  color: white;
  font-weight: 600;
}
.burst-btn--active:hover { filter: brightness(1.1); }

/* ── Settings gear button ────────────────────────────────────────────────────── */
.settings-wrap {
  position: relative;
  margin-left: auto;
  flex-shrink: 0;
}
.settings-btn {
  background: var(--slide-bg-card, white);
  border: 1.5px solid var(--slide-border, #CBD5E1);
  border-radius: 6px;
  padding: 2px 8px;
  font-size: 14px;
  line-height: 1.4;
  cursor: pointer;
  color: var(--slide-muted, #64748B);
  transition: border-color 0.18s, color 0.18s;
}
.settings-btn:hover,
.settings-btn.active {
  border-color: var(--accent-cyan, #028090);
  color: var(--accent-cyan, #028090);
}

/* ── Auto-Scaling menu (Mode 4) ──────────────────────────────────────────────── */
.autoscale-wrap {
  position: relative;
  flex-shrink: 0;
}
.autoscale-btn {
  background: var(--slide-bg-card, white);
  border: 1.5px solid var(--slide-border, #CBD5E1);
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 11px;
  font-family: inherit;
  cursor: pointer;
  color: var(--slide-fg, #1A2B3C);
  transition: border-color 0.18s, color 0.18s;
}
.autoscale-btn:hover,
.autoscale-btn.active {
  border-color: var(--accent-cyan, #028090);
  color: var(--accent-cyan, #028090);
}
.autoscale-label {
  font-size: 9.5px;
  color: var(--slide-muted, #64748B);
  font-weight: normal;
}
.autoscale-panel {
  position: absolute;
  left: 0;
  top: calc(100% + 5px);
  z-index: 30;
  background: var(--slide-bg-card, #ffffff);
  border: 1px solid var(--slide-border, #E2E8F0);
  border-radius: 8px;
  padding: 8px 10px 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.14);
  min-width: 260px;
  font-size: 10px;
}
.autoscale-strategy-pills {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-bottom: 6px;
}
.autoscale-hint {
  font-size: 9px;
  color: var(--slide-muted, #64748B);
  margin: 0 0 6px;
  line-height: 1.35;
}

/* ── Settings panel ──────────────────────────────────────────────────────────── */
.settings-panel {
  position: absolute;
  right: 0;
  top: calc(100% + 5px);
  z-index: 30;
  background: var(--slide-bg-card, #ffffff);
  border: 1px solid var(--slide-border, #E2E8F0);
  border-radius: 8px;
  padding: 8px 10px 10px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.14);
  min-width: 260px;
  font-size: 10px;
}
.sp-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10.5px;
  font-weight: bold;
  color: var(--slide-fg, #1A2B3C);
  margin-bottom: 8px;
  padding-bottom: 5px;
  border-bottom: 1px solid var(--slide-border, #E2E8F0);
}
.sp-close {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
  color: var(--slide-muted, #64748B);
  padding: 0 2px;
}
.sp-close:hover { color: var(--accent-red, #E63946); }

.sp-sep {
  height: 1px;
  background: var(--slide-border, #E2E8F0);
  margin: 6px 0;
}

.sp-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}
.sp-row:last-child { margin-bottom: 0; }

.sp-label {
  flex: 0 0 118px;
  color: var(--slide-muted, #64748B);
  font-size: 9.5px;
  white-space: nowrap;
}
.sp-sub {
  font-size: 8px;
  opacity: 0.75;
}
.sp-slider {
  flex: 1;
  accent-color: var(--accent-cyan, #028090);
  cursor: pointer;
  height: 4px;
}
.sp-val {
  flex: 0 0 68px;
  text-align: right;
  color: var(--slide-fg, #1A2B3C);
  font-size: 9.5px;
  font-weight: bold;
}
.sp-rand-label {
  color: var(--accent-purple, #7B5EA7);
  font-style: italic;
}

/* toggle switch */
.sp-row-toggle { margin-bottom: 0; }
.sp-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.sp-toggle input { display: none; }
.sp-toggle-track {
  position: relative;
  width: 28px; height: 14px;
  border-radius: 7px;
  background: var(--slide-border, #CBD5E1);
  transition: background 0.2s;
  flex-shrink: 0;
}
.sp-toggle-track.on {
  background: var(--accent-cyan, #028090);
}
.sp-toggle-thumb {
  position: absolute;
  top: 2px; left: 2px;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: white;
  transition: left 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}
.sp-toggle-track.on .sp-toggle-thumb {
  left: 16px;
}
.sp-toggle-lbl {
  font-size: 9.5px;
  font-weight: bold;
  color: var(--slide-fg, #1A2B3C);
  min-width: 20px;
}

/* settings panel transition */
.spanel-enter-active, .spanel-leave-active {
  transition: opacity 0.15s, transform 0.15s;
}
.spanel-enter-from, .spanel-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}

/* ── Canvas ──────────────────────────────────────────────────────────────────── */
.sd-canvas {
  flex: 1;
  min-height: 0;
  border-radius: 5px;
  overflow: hidden;
  background: var(--slide-bg, #F8FAFC);
}
.sd-canvas :deep(svg rect.sd-canvas-bg) {
  fill: var(--slide-bg, #F8FAFC);
}

/* ── Metrics ─────────────────────────────────────────────────────────────────── */
.sd-metrics { display: flex; gap: 5px; }
.metric {
  flex: 1;
  background: var(--slide-bg-card, white);
  border: 1px solid var(--slide-border, #E2E8F0);
  border-radius: 6px;
  padding: 4px 8px;
  text-align: center;
}
.m-label { font-size: 7.5px; color: var(--slide-muted, #94A3B8); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1px; }
.m-val   { font-size: 14px; font-weight: bold; color: var(--slide-fg, #1A2B3C); transition: color 0.3s; line-height: 1.2; }
.m-unit  { font-size: 8.5px; font-weight: normal; color: var(--slide-muted, #94A3B8); }
.m-note  { font-size: 7px; color: var(--slide-muted, #94A3B8); font-style: italic; }
.metric-lost {
  border-color: var(--accent-red, #E63946);
  background: color-mix(in srgb, var(--accent-red, #E63946) 8%, var(--slide-bg-card, white));
}

/* ── Overload glow ───────────────────────────────────────────────────────────── */
@keyframes overload-glow { 0%,100% { opacity:.10 } 50% { opacity:.22 } }
.overload-glow { animation: overload-glow 0.75s ease-in-out infinite; }

@keyframes restart-glow { 0%,100% { opacity:.12 } 50% { opacity:.25 } }
.restarting-glow { animation: restart-glow 0.75s ease-in-out infinite; }

/* ── Camera flash ────────────────────────────────────────────────────────────── */
.cam-flash { opacity: 0; pointer-events: none; }
.cam-flash.firing { opacity: 1; }
</style>
