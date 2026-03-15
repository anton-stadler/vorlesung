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
  <span class="accent-pink">#</span> Das Problem
</div>

<div class="scenario-label">
  <span class="accent-comment">// Szenario:</span> <span class="accent-cyan">Pizzabestellung in der Gruppe</span>
</div>

<ul style="font-size:0.82rem;line-height:1.9;margin-top:0.8rem;">
  <li>Einer läuft mit dem <span class="accent-orange">Zettel</span> rum und sammelt Bestellungen</li>
  <li>Kugelschreiber schreibt nicht — <em>hab ich jetzt schon einen Strich gemacht?</em></li>
  <li>Im Hintergrund <span class="accent-purple">quengeln die Kinder</span></li>
  <li>Anruf: <span class="accent-red">»Ach, ihr habt heute Ruhetag?«</span> — nächste Pizzeria</li>
  <li><span class="accent-red">»Keine Pizza Parma?«</span> — Bestellung überarbeiten</li>
  <li>Am Ende: <span class="accent-orange">eine Pizza fehlt.</span></li>
</ul>

<div class="problem-questions" style="display:flex;gap:0.6rem;margin-top:0.8rem;">
  <ProblemBox>Wer hat was bestellt?</ProblemBox>
  <ProblemBox>Was wurde storniert?</ProblemBox>
  <ProblemBox>Warum die falsche Pizza?</ProblemBox>
</div>

<div class="problem-insight" style="margin-top:0.8rem;">
  <span class="accent-comment">»</span>
  Am Ende kennt der Zettel nur den <span class="accent-orange">letzten Stand</span> —
  die <span class="accent-red">Geschichte ist verloren.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
routeAlias: demo
---

<!-- SLIDE 3 — DEMO -->

<div class="slide-header" style="margin-bottom:0.3rem;">
  <span class="accent-pink">#</span> Bestellt eure Pizza!
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

<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1.2rem;">

  <div style="border:1px solid var(--accent-cyan);border-radius:8px;padding:0.9rem 1.1rem;">
    <div class="col-title" style="color:var(--accent-cyan);font-size:0.82rem;margin-bottom:0.5rem;">
      🗄 Was der Zettel kennt
    </div>
    <div style="font-family:monospace;font-size:0.78rem;line-height:1.8;">
      <span class="muted">3×</span> Margherita<br>
      <span class="muted">2×</span> Salami<br>
      <span class="muted">1×</span> Funghi
    </div>
    <div class="muted" style="font-size:0.7rem;margin-top:0.8rem;">Nur der letzte Stand — kein Kontext.</div>
  </div>

  <div style="border:1px solid var(--accent-green,#4ade80);border-radius:8px;padding:0.9rem 1.1rem;">
    <div class="col-title" style="color:var(--accent-green,#4ade80);font-size:0.82rem;margin-bottom:0.5rem;">
      📜 Was passiert ist
    </div>
    <ul style="list-style:none;padding:0;margin:0;font-size:0.75rem;line-height:1.7;">
      <li><span class="accent-cyan">14:01</span> · Anna bestellt Margherita</li>
      <li><span class="accent-cyan">14:02</span> · Ben bestellt Salami</li>
      <li><span class="accent-orange">14:03</span> · Ben ändert → Hawaii</li>
      <li><span class="accent-red">14:05</span> · Pizzeria 1 hat Ruhetag</li>
      <li><span class="accent-red">14:06</span> · Ben storniert Hawaii (gibt's nicht)</li>
      <li><span class="accent-cyan">14:06</span> · Ben bestellt Funghi</li>
      <li><span class="accent-green">14:08</span> · Bestellung abgeschickt</li>
    </ul>
  </div>

</div>

<div class="problem-insight" style="margin-top:1.2rem;">
  <span class="accent-comment">»</span>
  Was wäre, wenn wir <span class="accent-green">jedes Ereignis</span> gespeichert hätten —
  statt nur den <span class="accent-orange">letzten Stand?</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 5 — DEMO: EVENT SOURCING AKTIVIEREN -->

<div class="slide-header" style="margin-bottom:0.3rem;">
  <span class="accent-pink">#</span> Demo: Event Sourcing aktivieren
</div>

<div style="overflow:hidden;border-radius:8px;height:430px;width:100%;">
  <iframe
    src="https://event-sourcing-d2lk.onrender.com/projector"
    style="width:166.67%;height:166.67%;max-width:none;border:none;display:block;transform:scale(0.6);transform-origin:top left;"
    allow="camera;microphone"
  />
</div>

---
layout: default-with-footer
---

<!-- SLIDE 6 — PYTHON MINIMALBEISPIEL -->

<div class="slide-header">
  <span class="accent-pink">#</span> Event Sourcing mit Python
</div>

<div class="scenario-label">
  <span class="accent-comment">// Minimalbeispiel:</span> <span class="accent-cyan">Append-only Event Store</span>
</div>

```python {lines:false}
@dataclass
class Event:
    type: str
    data: dict
    timestamp: datetime = field(default_factory=datetime.now)

event_store: list[Event] = []                    # Append-only!

def place_order(user: str, item: str):
    event_store.append(Event("item_added", {"user": user, "item": item}))

def cancel_order(user: str, item: str):
    event_store.append(Event("item_removed", {"user": user, "item": item}))

def get_current_orders() -> dict[str, list[str]]:  # Replay!
    orders = {}
    for e in event_store:
        u = e.data["user"]
        if e.type == "item_added":    orders.setdefault(u, []).append(e.data["item"])
        if e.type == "item_removed":  orders.get(u, []).remove(e.data["item"])
    return orders  # State aus Events berechnet — nie direkt gespeichert
```

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 7 — EINORDNUNG -->

<div class="slide-header"><span class="accent-pink">#</span> Einordnung: Wann Event Sourcing?</div>

::left::

<div class="col-title check">✓ Wann sinnvoll</div>

<ul class="check-list" style="font-size:0.78rem;">
  <li>Audit-Trail gesetzlich / regulatorisch erforderlich</li>
  <li>Komplexe Domäne mit vielen Zustandsübergängen</li>
  <li>Time-Travel &amp; Debugging sind geschäftskritisch</li>
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
  <span class="example-icon">🏥</span>
  <div>
    <div class="example-name">Patientenakte</div>
    <div class="example-desc muted">Lückenlose, unveränderliche Behandlungshistorie</div>
  </div>
</div>

::right::

<div class="col-title cross">✗ Wann Overkill</div>

<ul class="cross-list" style="font-size:0.78rem;">
  <li>Einfache CRUD-Apps ohne Historienrelevanz</li>
  <li>MVP / Prototyp unter Zeitdruck</li>
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
<div class="example-item">
  <span class="example-icon">🚀</span>
  <div>
    <div class="example-name">Startup-MVP</div>
    <div class="example-desc muted">Komplexität tötet Geschwindigkeit in früher Phase</div>
  </div>
</div>

::bottom::

<div class="problem-insight" style="margin:0;">
  <span class="accent-comment">»</span>
  Event Sourcing ist kein Ersatz für CRUD — es ist ein Werkzeug für Domänen,
  in denen die <span class="accent-green">Geschichte den Wert trägt.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 8 — VERTIEFUNG -->

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
