<template>
  <div style="display:flex;gap:1rem;justify-content:space-around;align-items:flex-start;">

    <!-- Vertical scaling: single drone → rocket -->
    <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
      <svg viewBox="0 0 200 185" width="200" height="185" xmlns="http://www.w3.org/2000/svg">
        <!-- Single drone (top) -->
        <line x1="72" y1="28" x2="127" y2="28" style="stroke:#64748b;" stroke-width="2.5" />
        <line x1="99" y1="15" x2="99" y2="41" style="stroke:#64748b;" stroke-width="2.5" />
        <rect x="86" y="20" width="26" height="16" rx="4" style="fill:#475569;stroke:#64748b;" stroke-width="1" />
        <circle cx="72" cy="28" r="7" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="127" cy="28" r="7" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="99" cy="15" r="7" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <circle cx="99" cy="41" r="7" style="fill:none;stroke:#94a3b8;" stroke-width="1.5" />
        <text x="100" y="57" style="fill:#94a3b8;font-size:9px;font-family:monospace;" text-anchor="middle">1 drone</text>
        <!-- Down arrow -->
        <text x="100" y="75" style="fill:#fb923c;font-size:20px;" text-anchor="middle">↓</text>
        <text x="100" y="89" style="fill:#94a3b8;font-size:8px;font-family:monospace;" text-anchor="middle">Vertical Scaling</text>
        <text x="100" y="99" style="fill:#64748b;font-size:7px;font-family:monospace;" text-anchor="middle">more power per unit</text>
        <!-- Rocket -->
        <rect x="86" y="108" width="28" height="55" rx="5" style="fill:#ef4444;stroke:#dc2626;" stroke-width="1.5" />
        <polygon points="86,108 114,108 100,92" style="fill:#dc2626;" />
        <polygon points="86,138 72,158 86,154" style="fill:#b91c1c;" />
        <polygon points="114,138 128,158 114,154" style="fill:#b91c1c;" />
        <ellipse cx="100" cy="165" rx="9" ry="5" style="fill:#fb923c;" opacity="0.85" />
        <ellipse cx="100" cy="171" rx="6" ry="4" style="fill:#fbbf24;" opacity="0.65" />
        <text x="100" y="183" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">Rocket — exponentially more expensive</text>
      </svg>
    </div>

    <!-- Horizontal scaling: drone swarm -->
    <div style="display:flex;flex-direction:column;align-items:center;flex:1;">
      <svg viewBox="0 0 240 185" width="240" height="185" xmlns="http://www.w3.org/2000/svg">
        <!-- Row 1: 4 drones -->
        <g transform="translate(10,8) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(65,4) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(122,8) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(178,3) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <!-- Row 2: 3 drones staggered -->
        <g transform="translate(38,44) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(96,40) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <g transform="translate(153,44) scale(0.55)">
          <line x1="0" y1="18" x2="55" y2="18" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <line x1="27" y1="5" x2="27" y2="31" style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2.5" />
          <rect x="14" y="10" width="26" height="16" rx="4" style="fill:#0ea5e9;stroke:#38bdf8;" stroke-width="1" />
          <circle cx="0" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="55" cy="18" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="5" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
          <circle cx="27" cy="31" r="7" style="fill:none;stroke:#38bdf8;" stroke-width="1.5" />
        </g>
        <!-- +∞ indicator -->
        <text x="120" y="91" style="fill:var(--accent-green,#4ade80);font-size:16px;font-weight:bold;" text-anchor="middle">+∞</text>
        <text x="120" y="103" style="fill:#94a3b8;font-size:8px;font-family:monospace;" text-anchor="middle">add as many as you like</text>
        <!-- Linear cost bar -->
        <rect x="20" y="112" width="200" height="14" rx="3" style="fill:#1e293b;stroke:#334155;" stroke-width="1" />
        <rect x="20" y="112" width="70" height="14" rx="3" style="fill:var(--accent-green,#4ade80);" opacity="0.35" />
        <text x="120" y="123" style="fill:var(--accent-green,#4ade80);font-size:7px;font-family:monospace;" text-anchor="middle">lineare Kosten · pay-per-use</text>
        <text x="120" y="144" style="fill:var(--accent-cyan,#38bdf8);font-size:9px;font-family:monospace;" text-anchor="middle">7 drones → 7× capacity</text>
        <text x="120" y="157" style="fill:#94a3b8;font-size:8px;font-family:monospace;" text-anchor="middle">1 fails → swarm continues</text>
        <text x="120" y="172" style="fill:#64748b;font-size:7px;font-family:monospace;" text-anchor="middle">no Single Point of Failure</text>
      </svg>
    </div>

  </div>
</template>
