# Ablauf: Event Sourcing als Architektur-Pattern mit Python

**Dauer:** ~20 Minuten | **Zielgruppe:** 4. Semester Bachelor Informatik

---

## Folie 1 — Cover (~30 s)

- Kurze Begrüßung, Vorstellung
- "Heute geht es um Event Sourcing — aber zuerst ein Problem, das ihr alle kennt."

---

## Folie 2 — Das Problem (~2 min)

**Anekdote erzählen — lebendig, mit Humor:**

> "Stellt euch vor: Pizzabestellung in der Gruppe. Einer läuft mit dem Zettel rum.
> Kugelschreiber schreibt nicht. Hab ich jetzt schon einen Strich gemacht?
> Im Hintergrund quengeln die Kinder. Dann wird angerufen:
> 'Ach, ihr habt heute Ruhetag?' — Nächste Pizzeria.
> 'Oh, ihr habt keine Pizza Parma?' — Bestellung überarbeiten.
> Und am Ende? Eine Pizza fehlt."

- Kurze Pause, dann auf die drei Fragen zeigen
- Insight vorlesen: "Am Ende kennt der Zettel nur den letzten Stand — die Geschichte ist verloren."
- **Überleitung:** "Genau dafür habe ich eine Demo programmiert. Probieren wir es aus!"

---

## Folie 3 — Demo Time! (~5 min)

### Vorbereitung
- [ ] Demo-App vorher aufrufen (Render-Coldstart dauert ~30s)
- [ ] Reset drücken, damit alles leer ist

### Ablauf
1. "Bestellt eure Pizza!" — QR-Code scannen lassen (Speisekarte)
2. Warten bis genug Bestellungen da sind (~1-2 min)
3. Auf den Projektor zeigen: "Schaut mal — was seht ihr?"
4. **Erkenntnis provozieren:** "Können wir sehen, wer was bestellt hat? Wer hat storniert? Nein!"
5. ggf. "Abschließen" drücken

### Steigerung (optional)
- "Tageskarte zeigen" → zweiter QR-Code erscheint
- Neue Bestellungen kommen rein → noch mehr Chaos

---

## Folie 4 — Was wäre wenn...? (~2 min)

- Gegenüberstellung zeigen: Zettel vs. Event-Log
- "Links: Das kennt unser System. Rechts: Das ist tatsächlich passiert."
- **Schlüsselfrage:** "Was wäre, wenn wir jedes Ereignis gespeichert hätten — statt nur den letzten Stand?"
- "Genau das ist Event Sourcing. Und unsere Demo kann das! Schauen wir nochmal rein."

---

## Folie 5 — Demo: Event Sourcing aktivieren (~3 min)

### Ablauf im iframe
1. **"Log einblenden"** klicken → Event-Stream erscheint
   - "Seht ihr? Jedes einzelne Ereignis. Wer, was, wann."
2. **"Personen einblenden"** klicken → Bestellungen nach Person
   - "Jetzt können wir nachvollziehen, wer was bestellt hat."
3. **"Replay"** klicken → Events werden nachgespielt
   - "Das ist Time-Travel. Wir spielen die gesamte Geschichte Schritt für Schritt nach."
   - **Das ist der Aha-Moment!**

---

## Folie 6 — Python Minimalbeispiel (~3 min)

- Code durchgehen:
  - `Event` Dataclass: type, data, timestamp
  - `event_store`: einfach eine Liste (append-only!)
  - `add_item` / `remove_item`: erzeugen Events, verändern keinen State direkt
  - `get_current_orders()`: berechnet den aktuellen Zustand durch **Replay aller Events**
- **Kernpunkt:** "Der State wird nie direkt verändert. Er wird immer aus den Events berechnet."

---

## Folie 7 — Einordnung: Wann Event Sourcing? (~2 min)

- Kurz durchgehen: Wann sinnvoll vs. Overkill
- "Kontobewegungen — das Lehrbuchbeispiel"
- "Aber für eine Todo-App? Overkill."
- **Insight vorlesen:** "Event Sourcing ist kein Ersatz für CRUD — es ist ein Werkzeug für Domänen, in denen die Geschichte den Wert trägt."

---

## Folie 8 — Vertiefung (BACKUP, ~2 min falls Zeit)

- Nur bei Fragen oder wenn Zeit übrig
- CQRS, Projektionen, Snapshots kurz antippen
- Idempotenz + Event Versioning als Ausblick

---

## Checkliste vor dem Vortrag

- [ ] Demo-App wach machen: `https://event-sourcing-d2lk.onrender.com/projector` aufrufen
- [ ] Reset drücken
- [ ] WLAN im Raum testen (Studenten brauchen Internet für QR-Scan)
- [ ] Backup-Plan: Falls kein WLAN → Screenshots der Demo zeigen
- [ ] Presenter-Modus in Slidev aktivieren (Taste `P`)
