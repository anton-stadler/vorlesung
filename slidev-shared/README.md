# Slidev Shared Addon (TH Rosenheim)

Gemeinsames **Slidev-Addon** für alle Rosenheim-Präsentationen. Enthält:

- **CSS:** `style.css` – Dracula-inspiriertes Farbschema, Cover/Layout-Klassen, Badges, etc.
- **Komponenten:** `ProblemBox`, `InfoCard`, `global-bottom.vue` (generische Fußzeile)

## Nutzung in einer Präsentation

### 1. Als lokales Paket installieren (empfohlen)

Im Präsentationsordner (dort wo `slides.md` und `package.json` liegen):

```bash
npm install ../slidev-shared
```

(Oder relativer Pfad zu `slidev-shared` von deinem Deck aus, z. B. bei `vorlesung/vorlesung2/` → `../slidev-shared`.)

In `package.json` erscheint z. B.:

```json
"slidev-addon-rosenheim-shared": "file:../slidev-shared"
```

### 2. Im Headmatter eintragen

In deiner `slides.md`:

```yaml
---
theme: neversink
addons:
  - prime
  - slidev-addon-rosenheim-shared
---
```

### Deck-spezifische Anpassungen

- **Fußzeile:** Wenn du einen anderen Text als „TH Rosenheim · 2026“ brauchst, leg in deinem Präsentationsordner eine eigene `components/global-bottom.vue` an – sie überschreibt die des Addons.
- **Weitere Komponenten:** Du kannst in deinem Deck jederzeit eigene `components/` und `style.css` (oder `styles/index.css`) ergänzen; sie werden mit dem Addon zusammengeführt.

## Wartung

Alle Änderungen an **CSS** und **gemeinsamen Komponenten** nur hier in `slidev-shared` vornehmen. Dann profitieren alle Präsentationen, die das Addon einbinden.
