---
theme: default
title: "Message-Based Architecture as an Enabler for Horizontally Scalable Hybrid AI Systems"
highlighter: shiki
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
  <div class="cover-tag">Probelehrveranstaltung · TH Rosenheim · 20.03.2026</div>

  <h1 class="cover-title">
    Message-Based Architecture<br>
    <span class="accent-pink">as an Enabler for</span><br>
    <span class="accent-cyan">Horizontally Scalable Hybrid AI Systems</span>
  </h1>

  <div class="cover-meta">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
    <div class="cover-org muted">Keenfinity GmbH · Bosch spin-off</div>
  </div>

  <div class="cover-footer">
    <span class="badge badge-purple">Master Informatik</span>
    <span class="badge badge-cyan">Applied AI</span>
    <span class="badge badge-blue">Distributed Systems</span>
    <span class="badge badge-pink">Cloud Computing</span>
  </div>

  <div class="cover-institution muted">
    Technische Hochschule Rosenheim · Fakultät für Informatik
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 2 — OPENER: HYBRID FIRE DETECTION -->

<div class="slide-header"><span class="accent-pink">#</span> Eine Kamera erkennt einen Brand — was passiert als nächstes?</div>

::left::

<div style="display:flex;justify-content:center;align-items:center;height:100%;">
  <FireDetectionSvg />
</div>

::right::

<div class="scenario-label">
  <span class="accent-comment">// System:</span>
  <span class="accent-cyan"> Hybrid Edge–Cloud AI</span>
</div>
<div class="example-item" style="margin-top:0.9rem;">
  <span class="example-icon" style="background:var(--accent-cyan,#38bdf8);color:white;padding:0.15rem 0.4rem;border-radius:4px;font-style:normal;font-size:0.65rem;min-width:auto;">EDGE</span>
  <div>
    <div class="example-name">Kamera + CNN erkennt Brand lokal</div>
    <div class="example-desc muted">Nur Alarm-Event wird gesendet — kein Video-Stream</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon" style="background:var(--accent-purple,#a78bfa);color:white;padding:0.15rem 0.4rem;border-radius:4px;font-style:normal;font-size:0.65rem;min-width:auto;">CLOUD</span>
  <div>
    <div class="example-name">Verification Model prüft den Alarm</div>
    <div class="example-desc muted">Passt Erkennungsschwelle θ adaptiv an</div>
  </div>
</div>

::bottom::

<div class="problem-insight">
  <span class="accent-comment">»</span>
  Was passiert, wenn <span class="accent-orange">1 000 Kameras</span> gleichzeitig einen Alarm senden?
  <span class="accent-comment">«</span>
</div>
<ul class="cross-list" style="margin-top:0.5rem;font-size:0.8rem;">
  <li>Wer nimmt Anfragen an, wenn der Worker abstürzt?</li>
  <li>Wie fügt man weitere Worker hinzu — ohne jede Kamera umzukonfigurieren?</li>
  <li>Wie verhindert man, dass Alarme verloren gehen?</li>
</ul>

---
layout: default-with-footer
routeAlias: demo
---

<!-- SLIDE 2 — LIVE DEMO -->

<div class="slide-header"><span class="accent-pink">#</span> Live Demo: Scaling Simulator</div>

<div style="flex:1;min-height:0;display:flex;flex-direction:column;">
  <ScalingDemo />
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 3 — MESSAGE BROKER -->

<div class="slide-header"><span class="accent-pink">#</span> Message Broker: Das Entkopplungsmuster</div>

::left::

<div class="col-title" style="color:var(--accent-red,#f87171);">⚡ Ohne Broker — Tight Coupling</div>

<ul class="cross-list" style="font-size:0.78rem;">
  <li>Producer kennt Adresse des Consumers</li>
  <li>Worker-Absturz → Alarm-Verlust</li>
  <li>Neuer Worker → alle Kameras umkonfigurieren</li>
</ul>

::right::

<div class="col-title" style="color:var(--accent-green,#4ade80);">✔ Mit Broker — Raum · Zeit · Anzahl</div>

<ul class="check-list" style="font-size:0.78rem;">
  <li><strong>Raum:</strong> Producer kennt Consumer-Adresse nicht</li>
  <li><strong>Zeit:</strong> Consumer kann offline sein — Nachrichten warten</li>
  <li><strong>Anzahl:</strong> Worker skalieren ohne Kamera-Änderung</li>
</ul>

::bottom::

<div style="margin-bottom:0.5rem;">
  <BrokerDiagramSvg />
</div>

<div style="display:flex;align-items:center;gap:1.2rem;margin-top:0.4rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    Der Broker ist kein Bottleneck — er ist der
    <span class="accent-orange">Entkopplungspunkt,</span>
    der horizontales Scaling erst <span class="accent-green">möglich macht.</span>
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 4 — SCALING: DRONE ANALOGY -->

<div class="slide-header"><span class="accent-pink">#</span> Gedankenexperiment: Wie greift man mit Drohnen an?</div>

::left::

<div class="col-title" style="color:var(--accent-orange,#fb923c);">↑ Vertikal: Größere Waffe</div>

<ul class="cross-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Physikalische Grenzen der Hardware</li>
  <li>Kosten steigen exponentiell</li>
  <li>Single Point of Failure</li>
</ul>

::right::

<div class="col-title" style="color:var(--accent-cyan,#38bdf8);">→ Horizontal: Drohnenschwarm</div>

<ul class="check-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Theoretisch unbegrenzte Kapazität</li>
  <li>Lineare Kosten — pay per use</li>
  <li>Ausfall einzelner Einheit unkritisch</li>
</ul>

::bottom::

<div style="margin-bottom:0.4rem;">
  <DroneScalingSvg />
</div>

<div style="display:flex;align-items:flex-end;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    <strong>Software-Analogie:</strong>
    Drohne = Worker-Pod · Rakete = Hochleistungsserver.
    Der Schwarm skaliert <span class="accent-cyan">horizontal</span> —
    und funktioniert nur mit <span class="accent-orange">Entkopplung über einen Message Broker.</span>
    <span class="muted" style="font-size:0.68rem;display:block;margin-top:0.25rem;">
      ℹ Historischer Kontext: Drohnenschwarm-Angriffe wurden u. a. im Ukraine-Krieg ab 2022 dokumentiert und gelten als Paradebeispiel für dezentrale Systemarchitektur.
    </span>
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 5 — AUTOSCALING -->

<div class="slide-header"><span class="accent-pink">#</span> Autoscaling: Der Schwarm wächst von selbst</div>

::left::

<div class="col-title" style="color:var(--accent-orange,#fb923c);">⚙ Reaktives Autoscaling</div>

<ul class="check-list" style="font-size:0.78rem;margin-top:0.3rem;">
  <li>Queue-Tiefe steigt → neue Worker-Pods starten automatisch</li>
  <li>Queue leer → überschüssige Pods werden beendet</li>
  <li>Kein manueller Eingriff nötig</li>
</ul>

<div class="examples-label accent-purple" style="margin-top:0.6rem;">Voraussetzung</div>
<div class="example-item">
  <span class="example-icon">🔗</span>
  <div>
    <div class="example-name">Stateless Worker</div>
    <div class="example-desc muted">Jeder Pod liest unabhängig aus der Queue — kein geteilter Zustand</div>
  </div>
</div>

::right::

<div class="col-title" style="color:var(--accent-cyan,#38bdf8);">☁ In der Cloud: KEDA / HPA</div>

<ul class="check-list" style="font-size:0.78rem;margin-top:0.3rem;">
  <li><strong>KEDA</strong> — skaliert Kubernetes-Pods anhand der Queue-Länge (RabbitMQ, Kafka, …)</li>
  <li><strong>HPA</strong> — Kubernetes Horizontal Pod Autoscaler auf CPU/Memory-Basis</li>
  <li>Kombination: Queue-Metrik + CPU → präzise Skalierung</li>
</ul>

<div class="example-item" style="margin-top:0.6rem;">
  <span class="example-icon">🏗</span>
  <div>
    <div class="example-name">Unser System</div>
    <div class="example-desc muted">1 000 Kamera-Alarme → Queue füllt sich → 20 Worker starten in &lt; 30 s</div>
  </div>
</div>

::bottom::

<div style="display:flex;align-items:center;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    Der Message Broker macht Autoscaling erst möglich — er entkoppelt
    <span class="accent-orange">Produktion</span> von <span class="accent-cyan">Verarbeitung</span>
    und liefert das Skalierungssignal gleich mit.
    <span class="accent-comment">«</span>
  </div>
</div>
