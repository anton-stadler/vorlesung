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
layout: default-with-footer
---

<!-- SLIDE 2 — OPENER: Hybride Brand Detektion -->

<div class="slide-header"><span class="accent-pink">#</span> Hybride Lösung für Brand Detektion</div>

<div class="opener-visual">
  <img src="/opener-hybrid-brand.svg" alt="Kamera erkennt Feuer → Request an Cloud → Cloud verarbeitet → Antwort zurück" class="opener-img" />
</div>

<p class="opener-teaser">
  Erkennung am <span class="accent-cyan">Rand</span> (Kamera), Verarbeitung in der <span class="accent-pink">Cloud</span> — so bleibt die Latenz niedrig und die Last skalierbar.
</p>

<div class="problem-insight">
  <span class="accent-comment">?</span>
  Was passiert, wenn <span class="accent-orange">viele Kameras gleichzeitig</span> einen Alarm melden?
</div>

---
layout: default-with-footer
routeAlias: demo
---

<!-- SLIDE 3 — LIVE DEMO (zentral, mehrfach aufrufbar) -->

<div class="slide-header"><span class="accent-pink">#</span> Live Demo: Scaling Simulator</div>

<div style="flex:1;min-height:0;display:flex;flex-direction:column;">
  <ScalingDemo />
</div>

---
layout: default-with-footer
---

<!-- SLIDE 4 — MESSAGE BROKER ÜBERSICHT + Zur Demo -->

<div class="slide-header"><span class="accent-pink">#</span> Message Broker — Übersicht</div>

<div class="scenario-label">
  <span class="accent-comment">// Idee:</span> Ein <span class="accent-cyan">Vermittler</span> zwischen Sendern und Empfängern. Keiner kennt die Adresse des anderen.
</div>

<ul class="check-list" style="margin-top: 0.8rem;">
  <li><strong>Entkopplung im Raum</strong> — Producer und Consumer können unabhängig ersetzt werden.</li>
  <li><strong>Entkopplung in der Zeit</strong> — Nachrichten bleiben liegen, wenn der Consumer gerade nicht da ist.</li>
  <li><strong>Entkopplung in der Anzahl</strong> — Beliebig viele Consumer können dieselbe Queue lesen; horizontal skalierbar.</li>
</ul>

<div class="problem-insight" style="margin-top: 0.8rem;">
  <span class="accent-comment">?</span>
  Was passiert in der Demo, wenn ihr den <span class="accent-orange">Broker abschaltet</span>?
</div>

<div style="margin-top: 1rem; display: flex; justify-content: center;">
  <DemoLink />
</div>

---
layout: default-with-footer
---

<!-- SLIDE 5 — HORIZONTAL VS. VERTIKAL: Drohnen-Beispiel -->

<div class="slide-header"><span class="accent-pink">#</span> Skalierung: vertikal vs. horizontal</div>

<div class="scenario-label">
  <span class="accent-comment">// Analogie (Vorlesungsbeispiel):</span> Eine Drohne als Ausgangslage — wie skaliert man?
</div>

<div class="opener-visual" style="margin: 0.6rem 0;">
  <img src="/scaling-drohnen.svg" alt="Eine Drohne · Vertikal: eine Rakete · Horizontal: Drohnenschwarm" class="opener-img" style="max-height: 200px;" />
</div>

<ul class="check-list" style="font-size: 0.9rem;">
  <li><strong>Vertikal:</strong> Eine <span class="accent-cyan">größere Einheit</span> (z. B. eine Rakete statt einer Drohne) — Grenzen durch Physik und Kosten.</li>
  <li><strong>Horizontal:</strong> <span class="accent-pink">Viele gleiche Einheiten</span> (Drohnenschwarm) — theoretisch beliebig skalierbar.</li>
</ul>

<div class="problem-insight" style="margin-top: 0.6rem;">
  <span class="accent-comment">?</span>
  In der Demo: <span class="accent-orange">vertikal</span> = größere Maschine, <span class="accent-cyan">horizontal</span> = mehr Worker. Wo sind die Grenzen?
</div>
