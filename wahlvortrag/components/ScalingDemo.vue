<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'

// ── Layout constants (SVG coordinate space 800 × 250) ─────────────────────────
const SVG_W = 800
const SVG_H = 250
const BRX = 305   // broker left x
const BRW = 155   // broker width
const BRY = 55    // broker top y
const BRH = 138   // broker height
const WRK_X = 590 // worker / server column start x

// ── Labels / tables ───────────────────────────────────────────────────────────
const VLABELS = ['small', 'medium', 'large', 'x-large']
const VRATES  = [3, 6, 12, 24]
const VCOSTS  = [0.50, 2.00, 8.00, 32.00]
const MTITLES = [
  'Direct Connection — No Broker',
  'Broker + Vertical Scaling',
  'Broker + Horizontal Scaling (Manual)',
  'Auto-Scale (KEDA)',
]

// ── State ─────────────────────────────────────────────────────────────────────
const mode          = ref(1)
const cameras       = ref(3)
const verticalSize  = ref(1)
const manualWorkers = ref(2)
const autoWorkers   = ref([{ id: 1, status: 'active', addedAt: 0, load: 0 }])
const queueLength   = ref(0)
const messagesLost  = ref(0)
const packets       = ref([])
const cameraFiring  = reactive({})  // { [index]: true/false } – reaktive Map pro Kamera
const PROCESSING_TIME_MS = 200
const FIRE_ANIM_MS  = 1000
const isBurst       = ref(false)
const canvasOpacity = ref(1)

const CAMERA_FIRES_PER_SEC = 2
const CAMERA_FIRE_INTERVAL_MS = 1000 / CAMERA_FIRES_PER_SEC  // 500 ms

let packetId    = 0
let workerId    = 1
let intervalId  = null
let cameraFireTimeoutId = null
let burstTimer  = null
let scaleUpCD   = 0
let scaleDownCD = 0
let cameraFireStopped = false  // true nach onUnmounted, damit kein neuer Timeout geplant wird
const MAX_PACKETS = 28

// ── Camera positions (lockerer Abstand, mind. 40px zwischen den Kameras) ───────
const camPositions = computed(() => {
  const n    = cameras.value
  const step = Math.max(40, (SVG_H - 50) / Math.max(n, 1))
  const total = (n - 1) * step
  const sy    = (SVG_H - total) / 2
  return Array.from({ length: n }, (_, i) => ({ x: 76, y: Math.round(sy + i * step) }))
})

// ── Worker grid helper ─────────────────────────────────────────────────────────
function workerGrid(count) {
  const cols = 2, bW = 74, bH = 38, gX = 8, gY = 8
  const rows  = Math.ceil(count / cols)
  const totH  = rows * bH + (rows - 1) * gY
  const sy    = Math.max(16, Math.round((SVG_H - totH) / 2))
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
const processingRate = computed(() => {
  if (mode.value <= 2) return VRATES[verticalSize.value - 1]
  if (mode.value === 3) return manualWorkers.value * 3
  return Math.max(autoWorkers.value.filter(w => w.status === 'active').length, 1) * 3
})
const incomingRate  = computed(() => cameras.value * 0.5)
const throughput    = computed(() => Math.round(Math.min(processingRate.value, incomingRate.value)))
const isOverloaded  = computed(() => mode.value === 1 && queueLength.value > 5)
const costPerHour   = computed(() => {
  if (mode.value <= 2) return VCOSTS[verticalSize.value - 1]
  if (mode.value === 3) return manualWorkers.value * 0.5
  return Math.max(autoWorkers.value.filter(w => w.status === 'active').length, 1) * 0.5
})

// Worker utilization: clamped ratio of incoming vs processing capacity
// Mode 1 & 2: one server with processingRate = VRATES[size]; Mode 3 & 4: active workers × 3 fps each
const workerUtilPct = computed(() => {
  const capacity = processingRate.value
  if (capacity <= 0) return 0
  return Math.min(1, incomingRate.value / capacity)
})

// Display load: 100% when queue is full, otherwise worker utilization
const effectiveLoad = computed(() =>
  queueLength.value >= 20 ? 1 : workerUtilPct.value
)

// Total latency (ms): queue wait + processing time per message
const latencyMs = computed(() => {
  const rate = processingRate.value
  if (rate <= 0) return null
  const queueWaitMs = (queueLength.value / rate) * 1000
  return Math.round(queueWaitMs + PROCESSING_TIME_MS)
})

const queueBarW  = computed(() => Math.round((Math.min(queueLength.value, 20) / 20) * (BRW - 22)))
const queueColor = computed(() => queueLength.value >= 8 ? '#E63946' : queueLength.value >= 5 ? '#F4A261' : '#028090')

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
    const camIdx = Math.floor(Math.random() * n)
    cameraFiring[camIdx] = true
    setTimeout(() => { cameraFiring[camIdx] = false }, FIRE_ANIM_MS)
  } finally {
    if (!cameraFireStopped) {
      cameraFireTimeoutId = setTimeout(fireOneCamera, CAMERA_FIRE_INTERVAL_MS)
    }
  }
}

// Kamera-Pakete nur noch über fireOneCamera (2×/s); Queue-Simulation läuft weiter im Tick
function spawnCameraPackets() {
  // Keine Paket-Spawns mehr hier – kontinuierliches Feuern über cameraFireIntervalId
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
    spawnPacket(BRX + BRW, BRY + BRH / 2, t.x, t.y, '#F4A261', 780)
  }
}

// ── KEDA ──────────────────────────────────────────────────────────────────────
function runKEDA() {
  const now = Date.now()
  const q   = queueLength.value
  autoWorkers.value.forEach(w => {
    if (w.status === 'starting' && now - w.addedAt >= 3000) w.status = 'active'
  })
  autoWorkers.value = autoWorkers.value.filter(w =>
    !(w.status === 'stopping' && now - w.stoppedAt >= 400)
  )
  const nonStopping = autoWorkers.value.filter(w => w.status !== 'stopping').length
  if (q > 3 && nonStopping < 8 && scaleUpCD <= 0) {
    autoWorkers.value.push({ id: ++workerId, status: 'starting', addedAt: now, load: 0 })
    scaleUpCD = 12
  }
  if (q < 1 && autoWorkers.value.filter(w => w.status === 'active').length > 1 && scaleDownCD <= 0) {
    const last = [...autoWorkers.value].reverse().find(w => w.status === 'active')
    if (last) { last.status = 'stopping'; last.stoppedAt = now; scaleDownCD = 25 }
  }
  if (scaleUpCD  > 0) scaleUpCD--
  if (scaleDownCD > 0) scaleDownCD--
}

// ── Tick ──────────────────────────────────────────────────────────────────────
function tick() {
  const inc   = incomingRate.value  * 0.2
  const proc  = processingRate.value * 0.2
  const wouldBe = queueLength.value + inc - proc
  if (wouldBe > 20) messagesLost.value += Math.round(wouldBe - 20)
  queueLength.value = Math.max(0, Math.min(20, wouldBe))
  if (mode.value === 4) runKEDA()
  spawnCameraPackets()
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
  if (isBurst.value) return
  isBurst.value = true
  const prev = cameras.value
  cameras.value = 10
  burstTimer = setTimeout(() => { cameras.value = prev; isBurst.value = false }, 5000)
}

onMounted(() => {
  cameraFireStopped = false
  intervalId = setInterval(tick, 200)
  cameraFireTimeoutId = setTimeout(fireOneCamera, CAMERA_FIRE_INTERVAL_MS)
})
onUnmounted(() => {
  cameraFireStopped = true
  clearInterval(intervalId)
  if (cameraFireTimeoutId) clearTimeout(cameraFireTimeoutId)
  if (burstTimer) clearTimeout(burstTimer)
})
</script>

<template>
  <div class="sd">

    <!-- Controls -->
    <div class="sd-ctrl">
      <div class="mode-pills">
        <button v-for="m in [1,2,3,4]" :key="m"
          class="mpill" :class="{ active: mode === m }" @click="switchMode(m)">
          Mode {{ m }}
        </button>
      </div>
      <div class="sliders-row">
        <label class="sl">
          Cameras <strong>{{ cameras }}</strong>
          <input type="range" min="1" max="10" v-model.number="cameras" />
        </label>
        <label v-if="mode <= 2" class="sl">
          Server <strong>{{ VLABELS[verticalSize - 1] }}</strong>
          <input type="range" min="1" max="4" v-model.number="verticalSize" />
        </label>
        <label v-if="mode === 3" class="sl">
          Workers <strong>{{ manualWorkers }}</strong>
          <input type="range" min="1" max="8" v-model.number="manualWorkers" />
        </label>
        <button v-if="mode === 4" class="burst-btn" :disabled="isBurst" @click="fireBurst">
          {{ isBurst ? '🔥 Bursting…' : '🔥 Fire burst!' }}
        </button>
      </div>
    </div>

    <!-- Mode title -->
    <div class="sd-mtitle">{{ MTITLES[mode - 1] }}</div>

    <!-- SVG Canvas -->
    <div class="sd-canvas" :style="{ opacity: canvasOpacity, transition: 'opacity 0.2s' }">
      <svg :width="SVG_W" :height="SVG_H" :viewBox="`0 0 ${SVG_W} ${SVG_H}`"
           xmlns="http://www.w3.org/2000/svg"
           style="width:100%;display:block;font-family:'JetBrains Mono',monospace;">

        <!-- Background -->
        <rect width="800" height="250" rx="6" fill="#F8FAFC" />

        <!-- ── Connector lines: cameras → target ── -->
        <line v-for="(cam, i) in camPositions" :key="`cl-${i}`"
          :x1="cam.x + 19" :y1="cam.y"
          :x2="mode === 1 ? sBox.x : BRX"
          :y2="mode === 1 ? sBox.y + sBox.h / 2 : BRY + BRH / 2"
          stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Connector: broker → server (Mode 2) -->
        <line v-if="mode === 2"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="sBox.x" :y2="sBox.y + sBox.h / 2"
          stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Connectors: broker → workers (Mode 3) -->
        <line v-if="mode === 3" v-for="(wp, i) in mode3Positions" :key="`wl3-${i}`"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="wp.x" :y2="wp.y + wp.h / 2"
          stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 3" />

        <!-- Connectors: broker → auto-workers (Mode 4) -->
        <line v-if="mode === 4" v-for="(wp, i) in mode4Positions" :key="`wl4-${i}`"
          :x1="BRX + BRW" :y1="BRY + BRH / 2"
          :x2="wp.x" :y2="wp.y + wp.h / 2"
          stroke="#CBD5E1" stroke-width="1" stroke-dasharray="4 3" />

        <!-- ── Left: Requests (incoming req/s) – with margin from cameras ── -->
        <g>
          <text x="22" y="118" text-anchor="middle" fill="#64748B" style="font-size:9px;font-weight:bold">Requests</text>
          <text x="22" y="132" text-anchor="middle" fill="#028090" style="font-size:11px;font-weight:bold">{{ incomingRate }}</text>
          <text x="22" y="144" text-anchor="middle" fill="#94A3B8" style="font-size:8px">req/s</text>
        </g>

        <!-- ── CAMERAS + Blitz-Kreis per CSS-Animation ── -->
        <g v-for="(cam, i) in camPositions" :key="`cam-${i}`">
          <!-- Blitz-Symbol: erscheint kurz rechts neben der Kamera -->
          <text :x="cam.x + 14" :y="cam.y + 4" style="font-size:14px"
                class="cam-flash" :class="{ firing: cameraFiring[i] }">⚡</text>
          <!-- Kamera-Icon -->
          <rect :x="cam.x - 12" :y="cam.y - 8"  width="16" height="12" rx="2" fill="#028090" />
          <circle :cx="cam.x - 4" :cy="cam.y - 2" r="4"   fill="#E2E8F0" />
          <circle :cx="cam.x - 4" :cy="cam.y - 2" r="2.5" fill="#028090" />
          <rect :x="cam.x - 10" :y="cam.y - 13" width="5" height="4" rx="1" fill="#028090" />
        </g>

        <!-- ── BROKER (Modes 2, 3, 4) ── -->
        <g v-if="mode > 1">
          <rect :x="BRX" :y="BRY" :width="BRW" :height="BRH"
                rx="7" fill="white" stroke="#F4A261" stroke-width="2" />
          <!-- icon row -->
          <text :x="BRX + 18" :y="BRY + 20" style="font-size:14px">📮</text>
          <text :x="BRX + 36" :y="BRY + 21" fill="#1A2B3C" font-weight="bold"
                style="font-size:11px">Message Broker</text>
          <!-- queue count -->
          <text :x="BRX + 11" :y="BRY + 38" fill="#64748B"
                style="font-size:9px">Queue: {{ Math.round(queueLength) }} / 20</text>
          <!-- bar bg -->
          <rect :x="BRX + 11" :y="BRY + 43" :width="BRW - 22" height="9" rx="4" fill="#E2E8F0" />
          <!-- bar fill -->
          <rect :x="BRX + 11" :y="BRY + 43" :width="queueBarW" height="9" rx="4" :fill="queueColor" />
          <!-- threshold ticks -->
          <line :x1="BRX + 11 + (5/20)*(BRW-22)" :y1="BRY + 42"
                :x2="BRX + 11 + (5/20)*(BRW-22)" :y2="BRY + 53"
                stroke="#F4A261" stroke-width="1.5" opacity="0.8" />
          <line :x1="BRX + 11 + (8/20)*(BRW-22)" :y1="BRY + 42"
                :x2="BRX + 11 + (8/20)*(BRW-22)" :y2="BRY + 53"
                stroke="#E63946" stroke-width="1.5" opacity="0.8" />
          <!-- bar labels -->
          <text :x="BRX + 11"       :y="BRY + 63" fill="#94A3B8" style="font-size:7.5px">0</text>
          <text :x="BRX + BRW - 11" :y="BRY + 63" text-anchor="end" fill="#94A3B8" style="font-size:7.5px">20</text>
          <!-- util section header -->
          <line :x1="BRX + 8" :y1="BRY + 72" :x2="BRX + BRW - 8" :y2="BRY + 72"
                stroke="#E2E8F0" stroke-width="1" />
          <text :x="BRX + 11" :y="BRY + 83" fill="#94A3B8" style="font-size:7.5px">Incoming rate</text>
          <text :x="BRX + BRW - 11" :y="BRY + 83" text-anchor="end" fill="#028090" font-weight="bold"
                style="font-size:8px">{{ incomingRate }} fps</text>
          <text :x="BRX + 11" :y="BRY + 96" fill="#94A3B8" style="font-size:7.5px">Processing rate</text>
          <text :x="BRX + BRW - 11" :y="BRY + 96" text-anchor="end" fill="#7B5EA7" font-weight="bold"
                style="font-size:8px">{{ processingRate }} fps</text>
          <!-- protocol label -->
          <text :x="BRX + BRW / 2" :y="BRY + BRH - 10" text-anchor="middle" fill="#94A3B8"
                style="font-size:7.5px;font-style:italic">MQTT / RabbitMQ</text>
          <!-- Throughput (successfully processed req/s) -->
          <text :x="BRX + BRW / 2" :y="BRY + BRH + 18" text-anchor="middle" fill="#64748B"
                style="font-size:8px">Throughput</text>
          <text :x="BRX + BRW / 2" :y="BRY + BRH + 32" text-anchor="middle" fill="#0D9488"
                style="font-size:11px;font-weight:bold">{{ throughput }} req/s</text>
        </g>

        <!-- ── Throughput (Mode 1: no broker) ── -->
        <g v-if="mode === 1">
          <text :x="(76 + sBox.x + sBox.w/2) / 2" :y="SVG_H - 28" text-anchor="middle" fill="#64748B"
                style="font-size:8px">Throughput</text>
          <text :x="(76 + sBox.x + sBox.w/2) / 2" :y="SVG_H - 14" text-anchor="middle" fill="#0D9488"
                style="font-size:11px;font-weight:bold">{{ throughput }} req/s</text>
        </g>

        <!-- ── SERVER (Modes 1 & 2) ── -->
        <g v-if="mode <= 2">
          <!-- Capacity (req/s) – more space above box -->
          <text :x="sBox.x + sBox.w/2" :y="sBox.y - 44" text-anchor="middle" fill="#64748B"
                style="font-size:8px">Capacity</text>
          <text :x="sBox.x + sBox.w/2" :y="sBox.y - 30" text-anchor="middle" fill="#7B5EA7"
                style="font-size:10px;font-weight:bold">{{ processingRate }} req/s</text>

          <rect v-if="isOverloaded"
                :x="sBox.x - 5" :y="sBox.y - 5" :width="sBox.w + 10" :height="sBox.h + 10"
                rx="11" fill="#E63946" class="overload-glow" />
          <rect :x="sBox.x" :y="sBox.y" :width="sBox.w" :height="sBox.h"
                rx="7" fill="white"
                :stroke="isOverloaded ? '#E63946' : '#E2E8F0'"
                :stroke-width="isOverloaded ? 2.5 : 1.5" />
          <!-- OVERLOADED badge (clear gap below Capacity) -->
          <g v-if="isOverloaded">
            <rect :x="sBox.x + sBox.w/2 - 33" :y="sBox.y - 19" width="66" height="16" rx="8" fill="#E63946" />
            <text :x="sBox.x + sBox.w/2" :y="sBox.y - 7"
                  text-anchor="middle" fill="white" font-weight="bold"
                  style="font-size:8px">OVERLOADED</text>
          </g>
          <!-- icon + size only -->
          <text :x="sBox.x + sBox.w/2" :y="sBox.y + sBox.h/2 - 8"
                text-anchor="middle" style="font-size:18px">🖥</text>
          <text :x="sBox.x + sBox.w/2" :y="sBox.y + sBox.h/2 + 14"
                text-anchor="middle" fill="#1A2B3C" font-weight="bold"
                style="font-size:11px">{{ VLABELS[verticalSize - 1] }}</text>
        </g>

        <!-- ── Right: Capacity (Mode 3) ── -->
        <g v-if="mode === 3">
          <text x="668" y="22" text-anchor="middle" fill="#64748B" style="font-size:8px">Capacity</text>
          <text x="668" y="36" text-anchor="middle" fill="#7B5EA7" style="font-size:10px;font-weight:bold">{{ processingRate }} req/s</text>
          <g v-for="(wp, i) in mode3Positions" :key="`w3-${i}`">
            <rect :x="wp.x" :y="wp.y" :width="wp.w" :height="wp.h"
                  rx="5" fill="white" stroke="#7B5EA7" stroke-width="1.5" />
            <!-- worker icon -->
            <text :x="wp.x + 12" :y="wp.y + 16" style="font-size:11px">⚙</text>
            <text :x="wp.x + 27" :y="wp.y + 15" fill="#1A2B3C" font-weight="bold"
                  style="font-size:9px">Pod {{ i + 1 }}</text>
          </g>
        </g>

        <!-- ── AUTO-SCALE WORKERS (Mode 4) ── -->
        <g v-if="mode === 4">
          <!-- KEDA badge -->
          <rect x="634" y="10" width="52" height="18" rx="9" fill="#7B5EA7" />
          <text x="660" y="23" text-anchor="middle" fill="white" font-weight="bold"
                style="font-size:9.5px">KEDA</text>
          <!-- Capacity (req/s) -->
          <text x="668" y="38" text-anchor="middle" fill="#64748B" style="font-size:8px">Capacity</text>
          <text x="668" y="52" text-anchor="middle" fill="#7B5EA7" style="font-size:10px;font-weight:bold">{{ processingRate }} req/s</text>

          <g v-for="(w, i) in autoWorkers" :key="w.id"
             :style="{ opacity: w.status === 'stopping' ? 0 : w.status === 'starting' ? 0.55 : 1,
                       transition: 'opacity 0.4s ease' }">
            <template v-if="mode4Positions[i]">
              <rect :x="mode4Positions[i].x" :y="mode4Positions[i].y"
                    :width="mode4Positions[i].w" :height="mode4Positions[i].h"
                    rx="5" fill="white"
                    :stroke="w.status === 'starting' ? '#F4A261' : '#7B5EA7'"
                    stroke-width="1.5" />
              <!-- icon -->
              <text :x="mode4Positions[i].x + 12" :y="mode4Positions[i].y + 16"
                    style="font-size:11px">
                {{ w.status === 'starting' ? '⏳' : '⚙' }}
              </text>
              <text :x="mode4Positions[i].x + 27" :y="mode4Positions[i].y + 15"
                    fill="#1A2B3C" font-weight="bold" style="font-size:9px">
                {{ w.status === 'starting' ? 'starting…' : `Pod ${i + 1}` }}
              </text>
            </template>
          </g>
        </g>

      </svg>
    </div>

    <!-- Metrics -->
    <div class="sd-metrics">
      <div v-if="mode > 1" class="metric">
        <div class="m-label">Queue</div>
        <div class="m-val" :style="{ color: queueLength >= 8 ? '#E63946' : queueLength >= 5 ? '#F4A261' : '' }">
          {{ Math.round(queueLength) }}<span class="m-unit"> / 20</span>
        </div>
      </div>
      <div class="metric">
        <div class="m-label">Load</div>
        <div class="m-val" :style="{ color: effectiveLoad >= 0.9 ? '#E63946' : effectiveLoad >= 0.6 ? '#F4A261' : '' }">
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
        <div class="m-label">Message lost</div>
        <div class="m-val" :style="{ color: messagesLost > 0 ? '#E63946' : '' }">{{ Math.round(messagesLost) }}</div>
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
/* ── Reset SVG font inheritance ─────────────────────────────────────────────── */
/* Force CSS to stop interfering with SVG text rendering */
.sd-canvas :deep(svg) { font-size: 1px !important; }
/* Individual SVG text elements use inline style="font-size:Xpx" to override */

/* ── Container ──────────────────────────────────────────────────────────────── */
.sd {
  font-family: 'JetBrains Mono', 'Consolas', monospace;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  padding: 9px 12px 7px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

/* ── Controls ───────────────────────────────────────────────────────────────── */
.sd-ctrl {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}
.mode-pills { display: flex; gap: 3px; }
.mpill {
  padding: 3px 10px;
  border-radius: 20px;
  border: 1.5px solid #CBD5E1;
  background: white;
  color: #1A2B3C;
  font-family: inherit;
  font-size: 11px;
  cursor: pointer;
  transition: background 0.18s, color 0.18s, border-color 0.18s;
}
.mpill.active  { background: #028090; color: white; border-color: #028090; }
.mpill:not(.active):hover { border-color: #028090; color: #028090; }

.sliders-row { display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.sl { display: flex; align-items: center; gap: 5px; font-size: 10.5px; color: #64748B; }
.sl strong { color: #1A2B3C; }
.sl input[type=range] { width: 85px; accent-color: #028090; cursor: pointer; }

.burst-btn {
  padding: 3px 11px;
  border-radius: 6px; border: none;
  background: #E63946; color: white;
  font-family: inherit; font-size: 11px;
  cursor: pointer; transition: opacity 0.2s;
}
.burst-btn:disabled { opacity: 0.55; cursor: not-allowed; }

/* ── Mode title ─────────────────────────────────────────────────────────────── */
.sd-mtitle { font-size: 11px; font-weight: bold; color: #028090; letter-spacing: 0.02em; }

/* ── Canvas ─────────────────────────────────────────────────────────────────── */
.sd-canvas { border-radius: 5px; overflow: hidden; }

/* ── Metrics ────────────────────────────────────────────────────────────────── */
.sd-metrics { display: flex; gap: 5px; }
.metric {
  flex: 1;
  background: white; border: 1px solid #E2E8F0; border-radius: 6px;
  padding: 4px 8px; text-align: center;
}
.m-label { font-size: 7.5px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 1px; }
.m-val   { font-size: 14px; font-weight: bold; color: #1A2B3C; transition: color 0.3s; line-height: 1.2; }
.m-unit  { font-size: 8.5px; font-weight: normal; color: #94A3B8; }
.m-note  { font-size: 7px; color: #94A3B8; font-style: italic; }
.metric-lost { border-color: #E63946; background: #FEF2F2; }

/* ── Overload glow ──────────────────────────────────────────────────────────── */
@keyframes overload-glow { 0%,100% { opacity:.10 } 50% { opacity:.22 } }
.overload-glow { animation: overload-glow 0.75s ease-in-out infinite; }

/* ── Kamera-Blitz ──────────────────────────────────────────────────────────── */
.cam-flash {
  opacity: 0;
  pointer-events: none;
}
.cam-flash.firing {
  opacity: 1;
}
</style>
