<template>
  <div style="display:flex;gap:0.5rem;justify-content:space-between;align-items:flex-start;">

    <!-- Left: tight coupling -->
    <svg viewBox="0 0 230 115" width="230" height="115" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="s3arrowR" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" style="fill:#f87171;" />
        </marker>
      </defs>
      <rect x="8" y="38" width="58" height="36" rx="4" style="fill:#1e293b;stroke:#f87171;" stroke-width="1.5" />
      <text x="37" y="54" style="fill:#94a3b8;font-size:9px;font-family:monospace;" text-anchor="middle">📷 Camera</text>
      <text x="37" y="67" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">HTTP POST</text>
      <line x1="66" y1="56" x2="158" y2="56" style="stroke:#f87171;" stroke-width="1.5" marker-end="url(#s3arrowR)" />
      <text x="112" y="49" style="fill:#94a3b8;font-size:8px;font-family:monospace;" text-anchor="middle">worker:8080</text>
      <rect x="158" y="38" width="64" height="36" rx="4" style="fill:#1e293b;stroke:#f87171;" stroke-width="1.5" />
      <text x="190" y="54" style="fill:#94a3b8;font-size:9px;font-family:monospace;" text-anchor="middle">⚙ Worker</text>
      <text x="190" y="67" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">feste Adresse</text>
      <line x1="168" y1="85" x2="212" y2="110" style="stroke:#f87171;" stroke-width="2" />
      <line x1="212" y1="85" x2="168" y2="110" style="stroke:#f87171;" stroke-width="2" />
      <text x="190" y="115" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">Absturz → Verlust</text>
    </svg>

    <!-- Right: with broker -->
    <svg viewBox="0 0 305 115" width="305" height="115" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="s3arrowO" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" style="fill:#fb923c;" />
        </marker>
        <marker id="s3arrowP" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
          <polygon points="0 0, 8 3, 0 6" style="fill:#a78bfa;" />
        </marker>
      </defs>
      <rect x="4" y="42" width="52" height="28" rx="3" style="fill:#1e293b;stroke:var(--accent-cyan,#38bdf8);" stroke-width="1.5" />
      <text x="30" y="59" style="fill:var(--accent-cyan,#38bdf8);font-size:9px;font-family:monospace;" text-anchor="middle">📷 Cam</text>
      <line x1="56" y1="56" x2="112" y2="56" style="stroke:#fb923c;" stroke-width="1.5" marker-end="url(#s3arrowO)" />
      <rect x="112" y="32" width="64" height="48" rx="4" style="fill:#1e293b;stroke:#fb923c;" stroke-width="2" />
      <text x="144" y="53" style="fill:#fb923c;font-size:9px;font-family:monospace;" text-anchor="middle">📮 Broker</text>
      <text x="144" y="66" style="fill:#64748b;font-size:8px;font-family:monospace;" text-anchor="middle">RabbitMQ</text>
      <line x1="176" y1="46" x2="224" y2="34" style="stroke:#a78bfa;" stroke-width="1.5" marker-end="url(#s3arrowP)" />
      <line x1="176" y1="56" x2="224" y2="56" style="stroke:#a78bfa;" stroke-width="1.5" marker-end="url(#s3arrowP)" />
      <line x1="176" y1="66" x2="224" y2="78" style="stroke:#a78bfa;" stroke-width="1.5" marker-end="url(#s3arrowP)" />
      <rect x="224" y="22" width="52" height="22" rx="3" style="fill:#1e293b;stroke:#a78bfa;" stroke-width="1.5" />
      <text x="250" y="37" style="fill:#a78bfa;font-size:8px;font-family:monospace;" text-anchor="middle">⚙ W1</text>
      <rect x="224" y="45" width="52" height="22" rx="3" style="fill:#1e293b;stroke:#a78bfa;" stroke-width="1.5" />
      <text x="250" y="60" style="fill:#a78bfa;font-size:8px;font-family:monospace;" text-anchor="middle">⚙ W2</text>
      <rect x="224" y="68" width="52" height="22" rx="3" style="fill:#1e293b;stroke:var(--accent-green,#4ade80);" stroke-width="1.5" stroke-dasharray="4,2" />
      <text x="250" y="83" style="fill:var(--accent-green,#4ade80);font-size:8px;font-family:monospace;" text-anchor="middle">+ W3 ✨</text>
    </svg>

  </div>
</template>
