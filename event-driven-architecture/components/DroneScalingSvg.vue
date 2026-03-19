<template>
  <div style="display:flex;gap:1rem;justify-content:space-around;align-items:flex-start;">

    <!-- Vertical scaling: drone (left) → rocket (right) -->
    <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
      <svg viewBox="0 0 340 160" width="340" height="160" xmlns="http://www.w3.org/2000/svg">
        <!-- Drone (left, centered at x=62, y=62) -->
        <line x1="30" y1="62" x2="95" y2="62" style="stroke:#64748b;" stroke-width="2.5" />
        <line x1="62" y1="46" x2="62" y2="78" style="stroke:#64748b;" stroke-width="2.5" />
        <rect x="48" y="54" width="28" height="18" rx="4" style="fill:#475569;stroke:#64748b;" stroke-width="1" />
        <circle cx="30" cy="62" r="8" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="95" cy="62" r="8" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="62" cy="46" r="8" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="62" cy="78" r="8" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <text x="62" y="100" style="fill:#94a3b8;font-size:10px;font-family:monospace;" text-anchor="middle">1 drone</text>
        <!-- Right arrow (center at x=165) -->
        <text x="165" y="68" style="fill:#fb923c;font-size:26px;" text-anchor="middle">→</text>
        <text x="165" y="90" style="fill:#94a3b8;font-size:9px;font-family:monospace;" text-anchor="middle">Vertical Scaling</text>
        <text x="165" y="102" style="fill:#64748b;font-size:8px;font-family:monospace;" text-anchor="middle">more power per unit</text>
        <!-- Rocket (right, centered at x=268) -->
        <polygon points="252,30 284,30 268,10" style="fill:#dc2626;" />
        <rect x="252" y="30" width="32" height="62" rx="5" style="fill:#ef4444;stroke:#dc2626;" stroke-width="1.5" />
        <polygon points="252,68 233,92 252,88" style="fill:#b91c1c;" />
        <polygon points="284,68 303,92 284,88" style="fill:#b91c1c;" />
        <ellipse cx="268" cy="94" rx="10" ry="6" style="fill:#fb923c;" opacity="0.85" />
        <ellipse cx="268" cy="101" rx="7" ry="5" style="fill:#fbbf24;" opacity="0.65" />
        <text x="268" y="120" style="fill:#f87171;font-size:9px;font-family:monospace;" text-anchor="middle">Rocket</text>
        <text x="268" y="132" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">costs grow super-linearly</text>
      </svg>
      <div class="scale-badges scale-badges-vertical">
        <span class="scale-badge scale-badge-up">Scale up</span>
        <span class="scale-badge scale-badge-down">Scale down</span>
      </div>
    </div>

    <!-- Horizontal scaling: drone swarm -->
    <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
      <svg viewBox="0 0 340 160" width="340" height="160" xmlns="http://www.w3.org/2000/svg">
        <!-- Row 1: 4 drones -->
        <g transform="translate(12,8) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(88,4) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(166,8) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(244,4) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <!-- Row 2: 3 drones staggered -->
        <g transform="translate(52,58) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(130,54) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(208,58) scale(0.72)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <!-- +∞ indicator -->
        <text x="170" y="122" style="fill:var(--accent-green,#4ade80);font-size:24px;font-weight:bold;" text-anchor="middle">+∞</text>
      </svg>
      <div class="scale-badges scale-badges-horizontal">
        <span class="scale-badge scale-badge-out">Scale out</span>
        <span class="scale-badge scale-badge-in">Scale in</span>
      </div>
    </div>

  </div>
</template>

<style scoped>
.scale-badges {
  display: flex;
  gap: 0.5rem;
  margin-top: -0.25rem;
  flex-wrap: wrap;
  justify-content: center;
}
.scale-badge {
  font-size: 0.7rem;
  font-family: var(--slidev-theme-font-mono, ui-monospace, monospace);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-weight: 600;
  white-space: nowrap;
}
.scale-badges-vertical .scale-badge-up {
  background: rgba(251, 146, 60, 0.2);
  color: var(--accent-orange, #fb923c);
  border: 1px solid rgba(251, 146, 60, 0.5);
}
.scale-badges-vertical .scale-badge-down {
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.4);
}
.scale-badges-horizontal .scale-badge-out {
  background: rgba(56, 189, 248, 0.2);
  color: var(--accent-cyan, #38bdf8);
  border: 1px solid rgba(56, 189, 248, 0.5);
}
.scale-badges-horizontal .scale-badge-in {
  background: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
  border: 1px solid rgba(148, 163, 184, 0.4);
}
</style>
