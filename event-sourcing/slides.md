---
theme: default
title: Event Sourcing als Architektur-Pattern mit Python
highlighter: shiki
shiki:
  themes:
    light: github-light
    dark: dracula
lineNumbers: false
colorSchema: auto
fonts:
  mono: JetBrains Mono
addons:
  - prime
  - slidev-addon-rosenheim-shared

---

<!-- SLIDE 1 — COVER -->
<div class="cover-wrap">
  <h1 class="cover-title">
    Event Sourcing<br>
    <span class="accent-pink">als Architektur-Pattern</span><br>
    <span class="accent-cyan">mit Python</span>
  </h1>

  <div class="cover-meta">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
    <div class="cover-footer">
      <span class="badge badge-cyan">Keenfinity GmbH · Bosch Ausgründung</span>
    </div>
  </div>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 2 — DAS PROBLEM -->

<div class="slide-header">
  <span class="accent-pink">#</span> Szenario: Pizza-Gruppenbestellung (Chaotisch)
</div>

<div style="display:flex;flex-direction:column;justify-content:space-between;flex:1;min-height:0;margin-top:0.5rem;">

  <div style="display:grid;grid-template-columns:1fr 9.5rem;align-items:center;row-gap:0.6rem;font-size:0.85rem;line-height:1.7;">
    <span>▪ Kugelschreiber schreibt nicht — <em>hab ich jetzt schon einen Strich gemacht?</em></span><span class="badge badge-cyan" style="white-space:nowrap;text-align:center;">Lost Write</span>
    <span>▪ Alle reden gleichzeitig auf den Besteller ein</span><span class="badge badge-purple" style="white-space:nowrap;text-align:center;">Overload</span>
    <span>▪ Das Kind <span class="accent-red">malt auf dem Zettel herum</span> — teilweise unleserlich</span><span class="badge badge-red" style="white-space:nowrap;text-align:center;">Hackerangriff</span>
    <span>▪ <span class="accent-red">»Dieses Gericht gibt's nicht mehr«</span> — Bestellung überarbeiten</span><span class="badge badge-orange" style="white-space:nowrap;text-align:center;">Breaking Change</span>
  </div>

  <div style="display:flex;flex-direction:column;gap:0.4rem;">
    <ProblemBox color="red" icon="!">Eine Pizza zu wenig.</ProblemBox>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;">
      <ProblemBox color="yellow">Wer hat was bestellt?</ProblemBox>
      <ProblemBox color="yellow">Was wurde storniert?</ProblemBox>
    </div>
  </div>

  <div class="problem-insight" style="margin:0;">
    <span class="accent-comment">»</span>
    Am Ende kennt der Zettel nur den <span class="accent-orange">letzten Stand</span> —
    die <span class="accent-red">Geschichte ist verloren.</span>
    <span class="accent-comment">«</span>
  </div>

</div>

---
layout: default-with-footer
routeAlias: demo
---

<!-- SLIDE 3 — DEMO -->

<div class="slide-header" style="margin-bottom:0.3rem;">
  <span class="accent-pink">#</span> Live-Demo: Pizza-Gruppenbestellung
</div>

<div style="overflow:hidden;border-radius:8px;height:420px;width:100%;">
  <iframe
    src="https://event-sourcing-d2lk.onrender.com/projector"
    style="width:142.86%;height:142.86%;max-width:none;border:none;display:block;transform:scale(0.7);transform-origin:top left;"
    allow="camera;microphone"
  />
</div>

---
layout: default-with-footer
---

<!-- SLIDE 4 — WAS WÄRE WENN -->

<div class="slide-header">
  <span class="accent-pink">#</span> Was wäre wenn...?
</div>

<div style="display:flex;flex-direction:column;justify-content:center;gap:1.2rem;flex:1;min-height:0;margin-top:0.5rem;">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">

<div style="border:1px solid var(--accent-cyan);border-radius:8px;padding:0.9rem 1.1rem;">
<div class="col-title" style="color:var(--accent-cyan);font-size:0.82rem;margin-bottom:0.5rem;">
🗄 Was der Zettel kennt
</div>
<div style="font-family:monospace;font-size:0.78rem;line-height:1.8;">
<span class="muted">3×</span> Margherita<br>
<span class="muted">2×</span> Salami<br>
<span class="muted">1×</span> Funghi
</div>
<div class="muted" style="font-size:0.7rem;margin-top:0.6rem;">Nur der letzte Stand — kein Kontext.</div>
</div>

<div style="border:1px solid var(--accent-green,#4ade80);border-radius:8px;padding:0.9rem 1.1rem;">
<div class="col-title" style="color:var(--accent-green,#4ade80);font-size:0.82rem;margin-bottom:0.5rem;">
📜 Was passiert ist
</div>
<ul style="list-style:none;padding:0;margin:0;font-size:0.75rem;line-height:1.75;">
<li><span class="accent-cyan">14:01</span> · Anna bestellt Margherita</li>
<li><span class="accent-cyan">14:02</span> · Ben bestellt Flötzinger</li>
<li><span class="accent-red">14:03</span> · Ben storniert Flötzinger</li>
<li><span class="accent-cyan">14:06</span> · Ben bestellt Auer</li>
<li><span class="accent-green">14:08</span> · Bestellung abgeschickt</li>
</ul>
</div>

</div>

<div class="problem-insight" style="margin:0;">
<span class="accent-comment">»</span>
Was wäre, wenn wir <span class="accent-green">jedes Ereignis</span> gespeichert hätten —
statt nur den <span class="accent-orange">letzten Stand?</span>
<span class="accent-comment">«</span>
</div>

</div>

---
layout: default-with-footer
---

<!-- SLIDE 6 — PYTHON MINIMALBEISPIEL -->

<div class="slide-header">
  <span class="accent-pink">#</span> Event Sourcing mit Python
</div>

<div style="max-height:410px;overflow-y:auto;border-radius:6px;">

<<< @/minimal-demo.py python

</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 7 — EINORDNUNG -->

<div class="slide-header"><span class="accent-pink">#</span> Einordnung: Wann Event Sourcing?</div>

::left::

<div class="col-title cross">✗ Wann Overkill</div>

<ul class="cross-list" style="font-size:0.78rem;">
  <li>Einfache Apps ohne Historienrelevanz</li>
  <li>Lesezugriffe dominieren stark</li>
</ul>

<div class="examples-label accent-purple">Praxis-Beispiele</div>

<div class="example-item">
  <span class="example-icon">📝</span>
  <div>
    <div class="example-name">Todo-App / Blog</div>
    <div class="example-desc muted">Kein Audit-Trail nötig — letzter Stand reicht</div>
  </div>
</div>

::right::

<div class="col-title check">✓ Wann sinnvoll</div>

<ul class="check-list" style="font-size:0.78rem;">
  <li>Audit-Trail gesetzlich / regulatorisch erforderlich</li>
  <li>Komplexe Domäne mit vielen Zustandsübergängen</li>
</ul>

<div class="examples-label accent-purple">Praxis-Beispiele</div>

<div class="example-item">
  <span class="example-icon">🏦</span>
  <div>
    <div class="example-name">Kontobewegungen</div>
    <div class="example-desc muted">Jede Transaktion ist ein Event</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">♟</span>
  <div>
    <div class="example-name">Schach (Multiplayer)</div>
    <div class="example-desc muted">Jeder Zug ist ein Event — Partie jederzeit rekonstruierbar</div>
  </div>
</div>

::bottom::

<div class="problem-insight" style="margin:0;">
  <span class="accent-comment">»</span>
  Event Sourcing ist kein universelles Muster — es ist ein Werkzeug für Domänen,
  in denen die <span class="accent-green">Geschichte den Wert trägt.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE — TAKEAWAYS -->

<div class="slide-header"><span class="accent-pink">#</span> Was wir heute gelernt haben.</div>

<div style="display:grid;grid-template-rows:repeat(4,1fr);gap:0.55rem;flex:1;min-height:0;margin-top:0.4rem;">

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-red,#f87171);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">🗑</div>
    <div>
      <div class="col-title" style="color:var(--accent-red,#f87171);font-size:0.95rem;">State speichern = Geschichte wegwerfen</div>
      <div class="muted" style="font-size:0.8rem;">UPDATE überschreibt — was vorher war, ist für immer verloren.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-green,#4ade80);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">📜</div>
    <div>
      <div class="col-title" style="color:var(--accent-green,#4ade80);font-size:0.95rem;">Events sind die Wahrheit — State ist abgeleitet</div>
      <div class="muted" style="font-size:0.8rem;">Nicht den Zustand speichern, sondern das, was passiert ist. Der Rest ergibt sich.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">⏪</div>
    <div>
      <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:0.95rem;">Zeitreise eingebaut</div>
      <div class="muted" style="font-size:0.8rem;">Replay bis Zeitpunkt X — jeder vergangene Zustand ist rekonstruierbar.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">🔮</div>
    <div>
      <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:0.95rem;">Neue Fragen — ohne neue Daten</div>
      <div class="muted" style="font-size:0.8rem;">Projektionen lassen sich nachträglich bauen — die Events sind schon da.</div>
    </div>
  </div>

</div>

---
layout: default
---

<!-- SLIDE 8 — THANKS -->

<div class="cover-wrap">
  <h1 class="cover-title" style="font-size:2.2rem;">Danke für die<br>
    <span class="accent-cyan">Aufmerksamkeit!</span>
  </h1>
  <div class="cover-meta" style="margin-top:1.5rem;">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
  </div>
</div>

---
layout: default
backup: true
---

<!-- SLIDE 9 — VERTIEFUNG -->

<div class="slide-header">
  <span class="accent-pink">#</span> Vertiefung &amp; verwandte Konzepte
  <span class="muted text-sm" style="font-size:0.65em; margin-left:0.5rem;">BACKUP</span>
</div>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.6rem;margin-top:0.5rem;">
  <InfoCard title="CQRS" icon="⇄" color="cyan">
    <template #subtitle>Command Query Responsibility Segregation</template>
    <ul>
      <li>Schreib- und Lesepfad <strong>konsequent trennen</strong></li>
      <li>Unabhängige Skalierung beider Seiten</li>
    </ul>
  </InfoCard>

  <InfoCard title="Projektionen" icon="⊕" color="purple">
    <template #subtitle>Read Models / Derived State</template>
    <ul>
      <li>Beliebig viele Sichten aus einem Event Log</li>
      <li>Änderungen <strong>rückwirkend</strong> möglich</li>
    </ul>
  </InfoCard>

  <InfoCard title="Snapshots" icon="📸" color="orange">
    <template #subtitle>Performance-Optimierung</template>
    <ul>
      <li>Periodisch State speichern</li>
      <li>Replay startet vom Snapshot, nicht Event #1</li>
    </ul>
  </InfoCard>
</div>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:0.6rem;margin-top:0.6rem;">
  <InfoCard title="Idempotenz" icon="🔁" color="green">
    <template #subtitle>Sichere Wiederholbarkeit</template>
    <ul>
      <li>Events können sicher wiederholt werden</li>
      <li>Wichtig bei Netzwerkfehlern &amp; Retries</li>
    </ul>
  </InfoCard>

  <InfoCard title="Event Versioning" icon="📋" color="pink">
    <template #subtitle>Schema-Evolution</template>
    <ul>
      <li>Event-Schemas ändern sich über die Zeit</li>
      <li>Upcasting: alte Events in neues Format transformieren</li>
    </ul>
  </InfoCard>
</div>
