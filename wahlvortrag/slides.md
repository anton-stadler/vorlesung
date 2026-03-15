---
theme: default
title: "Scalable Systems with Event-Driven Architecture"
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
    Scalable Systems<br>
    <span class="accent-cyan">with Event-Driven Architecture</span>
  </h1>

  <div class="cover-meta">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
    <div class="cover-footer">
      <span class="badge badge-cyan">Keenfinity GmbH · Bosch spin-off</span>
    </div>
  </div>
</div>

---
layout: two-cols-header-with-footer
showDemo: false
---

<!-- SLIDE 2 — OPENER: HYBRID FIRE DETECTION -->

<div class="slide-header"><span class="accent-pink">#</span> Edge meets Cloud: Hybrid Fire Detection</div>

::left::

<div style="display:flex;justify-content:center;align-items:flex-start;height:100%;padding-top:0.5rem;">
  <FireDetectionSvg />
</div>

::right::

<div class="example-item" style="margin-top:0.9rem;">
  <span class="example-icon badge-role badge-role-edge">Edge</span>
  <div style="text-align:left;">
    <div class="example-name">Small CNN · &lt; 50 ms · detects "fire possible"</div>
    <div class="example-desc muted">Sends only a compact image — no stream</div>
  </div>
</div>
<div class="example-item" style="margin-top:0.5rem;">
  <span class="example-icon badge-role badge-role-cloud">Cloud</span>
  <div style="text-align:left;">
    <div class="example-name">High-end model · &lt; 2 s · lower false-alarm rate</div>
    <div class="example-desc muted">Returns a confidence score</div>
  </div>
</div>

::bottom::

<div class="problem-insight">
  <span class="accent-comment">»</span>
  What happens when <span class="accent-orange">1,000 cameras</span> send an alarm at the same time?
  <span class="accent-comment">«</span>
</div>

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

<div class="slide-header"><span class="accent-pink">#</span> Message Broker: The Decoupling Pattern</div>

::left::

<div class="col-title" style="color:var(--accent-red,#f87171);">⚡ Without Broker — Tight Coupling</div>

<ul class="cross-list" style="font-size:0.78rem;">
  <li>Producer knows consumer's address</li>
  <li>Worker crash or overload → alarm loss</li>
  <li>New worker → reconfigure all cameras</li>
</ul>

::right::

<div class="col-title" style="color:var(--accent-green,#4ade80);">✔ With Broker — Space · Time · Count</div>

<ul class="check-list" style="font-size:0.78rem;">
  <li><strong>Space:</strong> Producer does not know consumer address</li>
  <li><strong>Time:</strong> Consumer can be offline — messages wait</li>
  <li><strong>Count:</strong> Scale workers without camera changes</li>
</ul>

::bottom::

<div style="margin-bottom:0.5rem;">
  <BrokerDiagramSvg />
</div>

<div style="display:flex;align-items:center;gap:1.2rem;margin-top:0.4rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    The broker is not a bottleneck — it is the
    <span class="accent-orange">decoupling point</span>
    that makes horizontal scaling <span class="accent-green">possible in the first place.</span>
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 4 — SCALING: DRONE ANALOGY -->

<div class="slide-header"><span class="accent-pink">#</span> Thought Experiment: One big unit vs. many small ones</div>

::left::

<div class="col-title" style="color:var(--accent-orange,#fb923c);">↑ Vertical: Bigger weapon</div>

<ul class="cross-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Physical limits of hardware</li>
  <li>Single point of failure</li>
</ul>
<ul class="check-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Lower latency — no network between components</li>
  <li>Simpler programming model — shared memory</li>
</ul>

::right::

<div class="col-title" style="color:var(--accent-cyan,#38bdf8);">→ Horizontal: Drone swarm</div>

<ul class="check-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Theoretically unlimited capacity</li>
  <li>Linear costs — pay per use</li>
</ul>
<ul class="cross-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Higher latency — network overhead between nodes</li>
  <li>More complex — distributed state &amp; coordination</li>
</ul>

::bottom::

<div style="margin-top:-1.2rem;">
  <DroneScalingSvg />
</div>
<div style="display:flex;align-items:flex-end;gap:1.2rem;margin-top:0.3rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    Drone = worker pod, Rocket = big server. Swarm scales <span class="accent-cyan">horizontally</span> — needs <span class="accent-orange">message broker.</span>
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 5 — AUTOSCALING -->

<div class="slide-header"><span class="accent-pink">#</span> Scale smart, not hard.</div>

::left::

<div class="examples-label accent-purple" style="font-size:0.78rem;">Requirements</div>
<ul class="check-list" style="font-size:0.78rem;margin-top:0.5rem;line-height:1.7;">
  <li><strong>Stateless</strong> — No shared state between pods.</li>
  <li><strong>Decoupling</strong> — Broker decouples producers and consumers.</li>
  <li><strong>Observability</strong> — Metrics available (queue, CPU, latency) and fast pod startup.</li>
</ul>
<div class="examples-label accent-purple" style="font-size:0.78rem;margin-top:1rem;">Tradeoff</div>
<ul class="check-list" style="font-size:0.78rem;margin-top:0.5rem;line-height:1.7;">
  <li><strong>Reliability</strong> — No message loss, delivery guarantees.</li>
  <li><strong>Cost</strong> — Keep resource spend low.</li>
  <li><strong>Latency</strong> — Meet SLAs, low wait times.</li>
</ul>

::right::

<div class="examples-label accent-cyan" style="font-size:0.78rem;margin-bottom:0.35rem;">Autoscaling metrics</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.4rem 0.5rem;margin-bottom:0.35rem;">
  <div class="metric-box" style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:6px;padding:0.35rem 0.5rem;">
    <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:0.78rem;">Queue</div>
    <div class="muted" style="font-size:0.7rem;">Scale by messages in queue (KEDA).</div>
  </div>
  <div class="metric-box" style="border:1px solid var(--accent-orange,#fb923c);border-radius:6px;padding:0.35rem 0.5rem;">
    <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:0.78rem;">Load / CPU</div>
    <div class="muted" style="font-size:0.7rem;">Scale by worker utilization (HPA).</div>
  </div>
  <div class="metric-box" style="border:1px solid var(--accent-purple,#bd93f9);border-radius:6px;padding:0.35rem 0.5rem;">
    <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:0.78rem;">Latency</div>
    <div class="muted" style="font-size:0.7rem;">Scale by queue wait time (SLA).</div>
  </div>
  <div class="metric-box" style="border:1px solid var(--accent-green,#16a34a);border-radius:6px;padding:0.35rem 0.5rem;">
    <div class="col-title" style="color:var(--accent-green,#16a34a);font-size:0.78rem;">Hybrid</div>
    <div class="muted" style="font-size:0.7rem;">Scale up when queue <strong>or</strong> latency exceeded; down when both relaxed.</div>
  </div>
</div>
<div class="muted" style="font-size:0.68rem;">… and many more options (custom metrics, Prometheus, etc.).</div>

::bottom::

<div style="display:flex;align-items:center;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    The broker enables autoscaling — it decouples senders and workers.<br>
    Metrics (queue, load, latency, …) tell when to scale.
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 6 — INDUSTRY STANDARDS -->

<div class="slide-header"><span class="accent-cyan">#</span> Further thoughts &amp; industry standards.</div>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-top:0.6rem;">

  <div class="metric-box" style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:1.2rem 1.4rem;">
    <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:0.9rem;margin-bottom:0.5rem;">☸ Kubernetes Ecosystem</div>
    <div style="font-size:0.82rem;line-height:1.6;"><strong>KEDA</strong> · <strong>HPA</strong> · <strong>VPA</strong> · <strong>Cluster Autoscaler</strong></div>
    <div class="muted" style="font-size:0.76rem;margin-top:0.4rem;">Industry standard for container-based autoscaling</div>
  </div>

  <div class="metric-box" style="border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:1.2rem 1.4rem;">
    <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:0.9rem;margin-bottom:0.5rem;">📈 Observability</div>
    <div style="font-size:0.82rem;line-height:1.6;"><strong>Prometheus</strong> · <strong>Grafana</strong> · <strong>OpenTelemetry</strong></div>
    <div class="muted" style="font-size:0.76rem;margin-top:0.4rem;">Metrics feed the scaler — no data, no scaling</div>
  </div>

  <div class="metric-box" style="border:1px solid var(--accent-green,#16a34a);border-radius:8px;padding:1.2rem 1.4rem;">
    <div class="col-title" style="color:var(--accent-green,#16a34a);font-size:0.9rem;margin-bottom:0.5rem;">⚡ Scale-to-Zero</div>
    <div style="font-size:0.82rem;line-height:1.6;"><strong>Cloud Run</strong> · <strong>Lambda</strong> · <strong>Knative</strong></div>
    <div class="muted" style="font-size:0.76rem;margin-top:0.4rem;">No load → no instances → no cost</div>
  </div>

  <div class="metric-box" style="border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:1.2rem 1.4rem;">
    <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:0.9rem;margin-bottom:0.5rem;">💸 FinOps</div>
    <div style="font-size:0.82rem;line-height:1.6;"><strong>Spot Instances</strong> · <strong>Predictive Scaling</strong></div>
    <div class="muted" style="font-size:0.76rem;margin-top:0.4rem;">Scale smart — optimize cost, not just capacity</div>
  </div>

</div>
