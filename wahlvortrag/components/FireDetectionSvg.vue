<template>
  <svg viewBox="0 0 380 290" width="360" height="275" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="s1arrowC" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" style="fill:var(--accent-cyan,#38bdf8)" />
      </marker>
      <marker id="s1arrowG" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
        <polygon points="0 0, 8 3, 0 6" style="fill:var(--accent-green,#4ade80)" />
      </marker>
    </defs>

    <!-- Building body -->
    <rect x="15" y="135" width="110" height="130" rx="3" style="fill:#1e293b;stroke:#475569;" stroke-width="1.5" />
    <!-- Windows -->
    <rect x="27" y="150" width="20" height="18" rx="1" style="fill:#f97316;" opacity="0.75" />
    <rect x="57" y="150" width="20" height="18" rx="1" style="fill:#f59e0b;" opacity="0.55" />
    <rect x="87" y="150" width="20" height="18" rx="1" style="fill:#1e293b;stroke:#334155;" stroke-width="1" />
    <rect x="27" y="183" width="20" height="18" rx="1" style="fill:#f97316;" opacity="0.35" />
    <rect x="57" y="183" width="20" height="18" rx="1" style="fill:#1e293b;stroke:#334155;" stroke-width="1" />
    <rect x="87" y="183" width="20" height="18" rx="1" style="fill:#1e293b;stroke:#334155;" stroke-width="1" />
    <!-- Door -->
    <rect x="55" y="225" width="30" height="40" rx="1" style="fill:#0f172a;" />

    <!-- Flames -->
    <path d="M15 265 Q28 238 44 255 Q50 222 66 244 Q72 210 84 238 Q91 207 103 234 Q109 212 120 252 Q128 230 140 265 Z" style="fill:#f97316;" opacity="0.95" />
    <path d="M28 265 Q40 246 54 257 Q59 234 70 250 Q75 225 86 246 Q92 224 102 244 Q108 232 116 258 Q122 240 130 265 Z" style="fill:#fbbf24;" opacity="0.8" />

    <!-- Camera housing -->
    <rect x="53" y="122" width="36" height="14" rx="2" style="fill:#475569;" />
    <rect x="58" y="113" width="24" height="12" rx="2" style="fill:#334155;" />
    <circle cx="70" cy="119" r="5" style="fill:var(--accent-cyan,#38bdf8);stroke:#0ea5e9;" stroke-width="1.5" />
    <circle cx="70" cy="119" r="2" style="fill:#0f172a;" />
    <rect x="68" y="134" width="5" height="8" style="fill:#475569;" />

    <!-- Arrow: camera → cloud -->
    <path d="M 106 115 C 165 72, 248 52, 290 62"
          style="stroke:var(--accent-cyan,#38bdf8);" stroke-width="2"
          fill="none" stroke-dasharray="6,3"
          marker-end="url(#s1arrowC)" />
    <!-- Alarm label background -->
    <rect x="155" y="57" width="100" height="20" rx="3"
          style="fill:#0f172a;stroke:var(--accent-cyan,#38bdf8);" stroke-width="1" opacity="0.95" />
    <text x="205" y="71" style="fill:var(--accent-cyan,#38bdf8);font-size:10px;font-family:monospace;" text-anchor="middle">alarm · ~1 KB JSON</text>

    <!-- Cloud bumps -->
    <ellipse cx="318" cy="82" rx="55" ry="22" style="fill:#1e293b;stroke:var(--accent-purple,#a78bfa);" stroke-width="1.5" />
    <circle cx="270" cy="77" r="15" style="fill:#1e293b;stroke:var(--accent-purple,#a78bfa);" stroke-width="1.5" />
    <circle cx="298" cy="64" r="17" style="fill:#1e293b;stroke:var(--accent-purple,#a78bfa);" stroke-width="1.5" />
    <circle cx="328" cy="59" r="19" style="fill:#1e293b;stroke:var(--accent-purple,#a78bfa);" stroke-width="1.5" />
    <circle cx="358" cy="67" r="15" style="fill:#1e293b;stroke:var(--accent-purple,#a78bfa);" stroke-width="1.5" />
    <!-- Cloud fill to hide seams -->
    <ellipse cx="318" cy="76" rx="52" ry="21" style="fill:#1e293b;" />
    <text x="318" y="72" style="fill:var(--accent-purple,#a78bfa);font-size:11px;font-family:monospace;font-weight:bold;" text-anchor="middle">AI Cloud</text>
    <text x="318" y="86" style="fill:#94a3b8;font-size:9px;font-family:monospace;" text-anchor="middle">Verification Model</text>

    <!-- Arrow: cloud → camera -->
    <path d="M 272 95 C 210 138, 152 162, 108 158"
          style="stroke:var(--accent-green,#4ade80);" stroke-width="2"
          fill="none" stroke-dasharray="6,3"
          marker-end="url(#s1arrowG)" />
    <!-- Response label background -->
    <rect x="147" y="150" width="100" height="20" rx="3"
          style="fill:#0f172a;stroke:var(--accent-green,#4ade80);" stroke-width="1" opacity="0.95" />
    <text x="197" y="164" style="fill:var(--accent-green,#4ade80);font-size:10px;font-family:monospace;" text-anchor="middle">θ = 0.94 · action</text>
  </svg>
</template>
