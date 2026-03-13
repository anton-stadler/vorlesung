---
theme: default
title: Event Sourcing als Architektur-Pattern mit Python
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
    Event Sourcing<br>
    <span class="accent-pink">als Architektur-Pattern</span><br>
    <span class="accent-cyan">mit Python</span>
  </h1>

  <div class="cover-meta">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
    <div class="cover-org muted">Keenfinity GmbH · Bosch Ausgründung</div>
  </div>

  <div class="cover-footer">
    <span class="badge badge-purple">4. Semester</span>
    <span class="badge badge-blue">Bachelor Informatik</span>
    <span class="badge badge-cyan">Cloud Computing</span>
    <span class="badge badge-pink">Applied AI</span>
    <span class="badge badge-green">Software Engineering</span>
  </div>

  <div class="cover-institution muted">
    Technische Hochschule Rosenheim · Fakultät für Informatik
  </div>
</div>

---
layout: default
---

<!-- SLIDE 2 — DAS PROBLEM -->

<div class="slide-header">
  <span class="accent-pink">#</span> Das Problem
</div>

<div class="scenario-label">
  <span class="accent-comment">// Szenario:</span> <span class="accent-cyan">Pizzabestellung in der Gruppe</span>
</div>

<div class="problem-layout">
  <div class="db-box">
    <div class="db-icon">🗄</div>
    <div class="db-name accent-cyan">orders</div>
    <div class="db-field">
      status = <span class="accent-green">'delivered'</span>
    </div>
  </div>

  <div class="problem-questions">
    <ProblemBox>Wer hat was bestellt?</ProblemBox>
    <ProblemBox>Was wurde storniert?</ProblemBox>
    <ProblemBox>Warum die falsche Pizza?</ProblemBox>
  </div>
</div>

<div class="problem-insight">
  <span class="accent-comment">»</span>
  Das klassische System kennt nur den <span class="accent-orange">aktuellen Zustand</span> —
  die <span class="accent-red">Geschichte ist verloren.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: two-cols-header
---

<!-- SLIDE 3 — EINORDNUNG -->

<div class="slide-header"><span class="accent-pink">#</span> Einordnung: Wann Event Sourcing?</div>

::left::

<div class="col-title check">✓ Wann sinnvoll</div>

<ul class="check-list">
  <li>Audit-Trail gesetzlich / regulatorisch erforderlich</li>
  <li>Komplexe Domäne mit vielen Zustandsübergängen</li>
  <li>Time-Travel &amp; Debugging sind geschäftskritisch</li>
  <li>Event-getriebene / kollaborative Systeme</li>
</ul>

<div class="examples-label accent-purple">Praxis-Beispiele</div>

<div class="example-item">
  <span class="example-icon">🏦</span>
  <div>
    <div class="example-name">Kontobewegungen</div>
    <div class="example-desc muted">Das Lehrbuchbeispiel — jede Transaktion ist ein Event</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">🛒</span>
  <div>
    <div class="example-name">E-Commerce Bestellung</div>
    <div class="example-desc muted">placed → paid → shipped → delivered → returned</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">🏥</span>
  <div>
    <div class="example-name">Patientenakte</div>
    <div class="example-desc muted">Lückenlose, unveränderliche Behandlungshistorie</div>
  </div>
</div>

::right::

<div class="col-title cross">✗ Wann Overkill</div>

<ul class="cross-list">
  <li>Einfache CRUD-Apps ohne Historienrelevanz</li>
  <li>Team ohne Event-Driven-Erfahrung</li>
  <li>Extrem hohes Event-Volumen ohne Snapshot-Plan</li>
  <li>Lesezugriffe dominieren stark</li>
  <li>MVP / Prototyp unter Zeitdruck</li>
</ul>

<div class="examples-label accent-purple">Praxis-Beispiele</div>

<div class="example-item">
  <span class="example-icon">📝</span>
  <div>
    <div class="example-name">Todo-App / Blog</div>
    <div class="example-desc muted">Kein Audit-Trail nötig — letzter Stand reicht</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">📊</span>
  <div>
    <div class="example-name">Reporting-Dashboard</div>
    <div class="example-desc muted">Lesedominant — Event Store bringt keinen Mehrwert</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">🚀</span>
  <div>
    <div class="example-name">Startup-MVP</div>
    <div class="example-desc muted">Komplexität tötet Geschwindigkeit in früher Phase</div>
  </div>
</div>

---
layout: default
---

<!-- SLIDE 4 — BACKUP: VERTIEFUNG -->

<div class="slide-header">
  <span class="accent-pink">#</span> Vertiefung &amp; verwandte Konzepte
  <span class="muted text-sm" style="font-size:0.65em; margin-left:0.5rem;">BACKUP</span>
</div>

<div class="cards-grid">
  <InfoCard title="CQRS" icon="⇄" color="cyan">
    <template #subtitle>Command Query Responsibility Segregation</template>
    <ul>
      <li>Schreib- und Lesepfad <strong>konsequent trennen</strong></li>
      <li>Event Store schreibt, optimierte Read Models lesen</li>
      <li>Ermöglicht unabhängige Skalierung beider Seiten</li>
    </ul>
  </InfoCard>

  <InfoCard title="Projektionen & Read Models" icon="⊕" color="purple">
    <template #subtitle>Derived State</template>
    <ul>
      <li>Beliebig viele Sichten aus einem Event Log</li>
      <li>Nach Kunde · nach Produkt · nach Zeitraum</li>
      <li>Änderungen <strong>rückwirkend</strong> möglich</li>
    </ul>
  </InfoCard>

  <InfoCard title="Snapshots" icon="📸" color="orange">
    <template #subtitle>Performance-Optimierung</template>
    <ul>
      <li>Bei langen Event-Streams wird Replay teuer</li>
      <li>Snapshots speichern periodisch den State</li>
      <li>Replay startet vom letzten Snapshot, nicht Event #1</li>
    </ul>
  </InfoCard>
</div>
