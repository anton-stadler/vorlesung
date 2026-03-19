# Plan: Queue-Befüllung ereignisbasiert (Message-Broker)

## Problem

Aktuell wird die Broker-Queue **nicht** bei jeder eingehenden Nachricht gefüllt, sondern über eine **durchschnittliche Rate** im Tick:

- **Tick (alle 200 ms):** `inc = incomingRate * 0.2` wird zur Queue addiert → gleichmäßiger Zufluss.
- **fireOneCamera():** Wird durch den Randomizer zeitlich variabel aufgerufen (Blitz, Linien-Style), **erhöht die Queue aber nicht**.

Folge: Die Anzeige der Queue reagiert nicht auf die tatsächlichen „Feuer“-Ereignisse; der Randomizer beeinflusst nur die Optik, nicht die Queue-Logik.

---

## Ziel

- **Eine eingehende Nachricht** = ein Aufruf von `fireOneCamera()` (ein Blitz).
- **Bei jeder solchen Nachricht** (nur in Broker-Modi): Queue um 1 erhöhen (bis max. 20), sonst `messagesLost` erhöhen.
- **Tick** regelt nur noch den **Abgang** (Verarbeitung) und KEDA/spawnBrokerPackets; **kein** Zufluss mehr über `inc`.

Dann wird die Queue durch die echten Events (inkl. Randomizer) befüllt und wirkt z. B. bei „burstig“/„chaotisch“ tatsächlich burstig.

---

## Schritte zur Umsetzung

### 1. Queue-Zugang in `fireOneCamera()` (ereignisbasiert)

**Datei:** `ScalingDemo.vue`, Funktion `fireOneCamera()`.

- **Nach** dem Setzen von `cameraFiring[idx]` (und nur wenn Broker aktiv):
  - Wenn `mode.value > 1`:
    - Wenn `queueLength.value < 20`: `queueLength.value += 1`
    - Sonst: `messagesLost.value += 1` (Nachricht verworfen, Queue voll)
- In Mode 1 (Direct) keine Queue-Änderung (kein Broker).

So entspricht **ein Blitz = eine Nachricht = +1 Queue** (bzw. +1 Lost bei voller Queue).

### 2. Tick: Zufluss entfernen, nur noch Abgang

**Datei:** `ScalingDemo.vue`, Funktion `tick()`.

- **Entfernen:** Berechnung und Verwendung von `inc` (kein `incomingRate * 0.2` mehr zur Queue addieren).
- **Beibehalten:**
  - Abgang: `proc = processingRate.value * 0.2`, `queueLength.value = max(0, min(20, queueLength.value - proc))`.
  - Optional: Wenn du Nachrichtenverlust nur bei Überlauf beim **Zugang** zählst, kannst du die Zeile `if (wouldBe > 20) messagesLost += ...` im Tick streichen (Verlust passiert dann nur in `fireOneCamera()` bei vollem Puffer).
- **Unverändert:** `runKEDA()` (Mode 4), `spawnBrokerPackets()`.

### 3. Konsistenz prüfen

- **Anzeige „Requests“ / incomingRate:** Unverändert als Durchschnitt (cameras × ratePerCamera). Passt weiterhin als Kennzahl.
- **messagesLost:** Wird bei vollem Puffer in `fireOneCamera()` erhöht; ggf. im Tick keine doppelte Zählung mehr (siehe Schritt 2).
- **Randomizer:** Beeinflusst weiterhin nur `getFireDelay()`; durch die neue Queue-Logik führt „burstig“/„chaotisch“ nun auch zu burstiger Queue-Füllung.

### 4. Optional: Verarbeitungs-Abgang feiner auflösen

Falls gewünscht: Statt pro Tick einen Anteil `proc` abzuziehen, könnte man bei jeder „verarbeiteten“ Nachricht (z. B. wenn ein Broker→Worker-Packet gespawnt wird) die Queue um 1 verringern. Das wäre ein zweiter Schritt für noch stärkere Ereignis-Orientierung; für die Korrektur „Queue wird bei eingehender Message befüllt“ reichen Schritte 1 und 2.

---

## Kurzfassung

| Wo            | Änderung |
|---------------|----------|
| `fireOneCamera()` | Bei `mode > 1`: `queueLength += 1` (max 20), sonst `messagesLost += 1`. |
| `tick()`      | Kein `inc` mehr; nur noch Abzug `proc` von `queueLength`; KEDA/spawnBrokerPackets unverändert. |
| Verlust-Zählung | Nur noch in `fireOneCamera()` bei vollem Puffer (oder im Tick belassen, aber nicht doppelt zählen). |

Damit wird der Message-Broker genau dann befüllt, wenn eine Nachricht reinkommt (Blitz), und der Randomizer wirkt sich auf die Queue aus.
