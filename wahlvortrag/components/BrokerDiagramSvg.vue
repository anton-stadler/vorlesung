<template>
  <div style="display:flex;gap:1.5rem;justify-content:space-around;align-items:center;width:100%;">

    <!-- Left: tight coupling -->
    <div style="flex:1;max-width:320px;">
      <svg viewBox="0 0 260 130" width="100%" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="s3arrowR" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" style="fill:#f87171;" />
          </marker>
        </defs>
        <!-- Camera box -->
        <rect x="8" y="38" width="70" height="40" rx="5" fill="transparent" stroke="#f87171" stroke-width="2" />
        <text x="43" y="55" style="fill:#f87171;font-size:10px;font-family:monospace;" text-anchor="middle">📷 Camera</text>
        <text x="43" y="70" style="fill:#f87171;font-size:9px;font-family:monospace;" text-anchor="middle">HTTP POST</text>
        <!-- Arrow with hard-coded address label -->
        <line x1="78" y1="58" x2="172" y2="58" stroke="#f87171" stroke-width="2" marker-end="url(#s3arrowR)" />
        <text x="125" y="50" style="fill:currentColor;font-size:9px;font-family:monospace;opacity:0.7;" text-anchor="middle">worker:8080</text>
        <!-- Worker box -->
        <rect x="172" y="38" width="78" height="40" rx="5" fill="transparent" stroke="#f87171" stroke-width="2" />
        <text x="211" y="55" style="fill:currentColor;font-size:10px;font-family:monospace;" text-anchor="middle">⚙ Worker</text>
        <text x="211" y="70" style="fill:#f87171;font-size:9px;font-family:monospace;" text-anchor="middle">feste Adresse</text>
        <!-- Crash X -->
        <line x1="190" y1="90" x2="232" y2="120" stroke="#f87171" stroke-width="2.5" />
        <line x1="232" y1="90" x2="190" y2="120" stroke="#f87171" stroke-width="2.5" />
        <text x="211" y="130" style="fill:#f87171;font-size:8px;font-family:monospace;" text-anchor="middle">Absturz → Verlust</text>
      </svg>
    </div>

    <!-- Right: with broker — FOCUS ON DECOUPLING -->
    <div style="flex:1;max-width:400px;">
      <svg viewBox="0 0 340 130" width="100%" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="s3arrowO" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" style="fill:#fb923c;" />
          </marker>
          <marker id="s3arrowP" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <polygon points="0 0, 8 3, 0 6" style="fill:#a78bfa;" />
          </marker>
        </defs>

        <!-- Camera box -->
        <rect x="4" y="45" width="66" height="38" rx="5" fill="transparent" stroke="var(--accent-cyan,#38bdf8)" stroke-width="2" />
        <text x="37" y="62" style="fill:var(--accent-cyan,#38bdf8);font-size:10px;font-family:monospace;" text-anchor="middle">📷 Camera</text>
        <text x="37" y="76" style="fill:currentColor;font-size:8px;font-family:monospace;opacity:0.6;" text-anchor="middle">HTTP POST</text>

        <!-- Arrow Cam → Broker with topic label -->
        <line x1="70" y1="64" x2="128" y2="64" stroke="#fb923c" stroke-width="2" marker-end="url(#s3arrowO)" />
        <text x="99" y="56" style="fill:#fb923c;font-size:8px;font-family:monospace;" text-anchor="middle">"fire.alarm"</text>

        <!-- Broker box — prominent -->
        <rect x="128" y="30" width="90" height="66" rx="6" fill="transparent" stroke="#fb923c" stroke-width="2.5" />
        <text x="173" y="54" style="fill:#fb923c;font-size:11px;font-family:monospace;font-weight:bold;" text-anchor="middle">📮 Broker</text>
        <text x="173" y="68" style="fill:currentColor;font-size:8px;font-family:monospace;opacity:0.6;" text-anchor="middle">RabbitMQ</text>
        <text x="173" y="82" style="fill:currentColor;font-size:8px;font-family:monospace;opacity:0.5;" text-anchor="middle">Queue</text>

        <!-- Arrow Broker → Worker -->
        <line x1="218" y1="64" x2="255" y2="64" stroke="#a78bfa" stroke-width="2" marker-end="url(#s3arrowP)" />

        <!-- Vertical decoupling divider line (after arrow tip, before worker box) -->
        <line x1="263" y1="8" x2="263" y2="122" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.35" />
        <text x="263" y="5" style="fill:currentColor;font-size:7px;font-family:monospace;opacity:0.5;" text-anchor="middle">kein direkter Kontakt</text>

        <!-- Worker box -->
        <rect x="268" y="45" width="68" height="38" rx="5" fill="transparent" stroke="#a78bfa" stroke-width="2" />
        <text x="302" y="62" style="fill:#a78bfa;font-size:10px;font-family:monospace;" text-anchor="middle">⚙ Worker</text>
        <text x="302" y="76" style="fill:currentColor;font-size:8px;font-family:monospace;opacity:0.6;" text-anchor="middle">beliebig viele</text>
      </svg>
    </div>

  </div>
</template>
