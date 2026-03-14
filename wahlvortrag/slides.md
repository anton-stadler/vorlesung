---
theme: default
title: "Scalable Systems via Message-Based Architecture"
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
  <div class="cover-tag">Trial Lecture · TH Rosenheim · 20.03.2026</div>

  <h1 class="cover-title">
    Scalable Systems<br>
    <span class="accent-cyan">via Message-Based Architecture</span>
  </h1>

  <div class="cover-meta">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
    <div class="cover-org muted">Keenfinity GmbH · Bosch spin-off</div>
  </div>

  <div class="cover-footer">
    <span class="badge badge-purple">Master Computer Science</span>
    <span class="badge badge-cyan">Applied AI</span>
    <span class="badge badge-blue">Distributed Systems</span>
    <span class="badge badge-pink">Cloud Computing</span>
  </div>

  <div class="cover-institution muted">
    Rosenheim University of Applied Sciences · Faculty of Computer Science
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

<div class="scenario-label">
  <span class="accent-comment">// Strategy:</span>
  <span class="accent-cyan"> Hybrid Edge–Cloud AI</span>
</div>
<div class="example-item" style="margin-top:0.9rem;">
  <span class="example-icon badge-role badge-role-edge">Edge</span>
  <div style="text-align:left;">
    <div class="example-name">Small CNN model on the camera</div>
    <div class="example-desc muted">Real-time inference &lt; 50 ms · detects "fire possible"</div>
    <div class="example-desc muted">Only a compact image is sent — no stream</div>
  </div>
</div>
<div class="example-item" style="margin-top:0.5rem;">
  <span class="example-icon badge-role badge-role-cloud">Cloud</span>
  <div style="text-align:left;">
    <div class="example-name">High-end model in the cloud</div>
    <div class="example-desc muted">Latency &lt; 2 s allowed · lower false-alarm rate</div>
    <div class="example-desc muted">Returns a confidence score</div>
  </div>
</div>
<div class="problem-insight" style="margin-top:0.8rem;font-size:0.78rem;">
  <span class="accent-comment">»</span>
  Why hybrid? Real-time needs a <span class="accent-cyan">small model locally</span> —
  precision needs a <span class="accent-purple">large model in the cloud.</span>
  <span class="accent-comment">«</span>
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
  <li>Worker crash → alarm loss</li>
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

<div style="margin-bottom:0.4rem;">
  <DroneScalingSvg />
</div>

<div style="display:flex;align-items:flex-end;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    <strong>Software analogy:</strong>
    Drone = worker pod · Rocket = high-performance server.
    The swarm scales <span class="accent-cyan">horizontally</span> —
    and only works with <span class="accent-orange">decoupling via a message broker.</span>
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

<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-top:0.5rem;flex:1;">

  <!-- Block 1: Kubernetes Ecosystem -->
  <div class="metric-box" style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:0.55rem 0.7rem;">
    <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:0.78rem;margin-bottom:0.3rem;">
      ☸ Kubernetes Ecosystem
    </div>
    <ul style="margin:0;padding-left:1.1rem;font-size:0.7rem;line-height:1.75;">
      <li><strong>KEDA</strong> — Event-driven Autoscaler (Queue, Kafka, HTTP triggers)</li>
      <li><strong>HPA</strong> — Horizontal Pod Autoscaler (CPU, Memory, custom metrics)</li>
      <li><strong>VPA</strong> — Vertical Pod Autoscaler (right-size resource requests)</li>
      <li><strong>Cluster Autoscaler</strong> — adds/removes nodes on demand</li>
    </ul>
  </div>

  <!-- Block 2: Observability Stack -->
  <div class="metric-box" style="border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:0.55rem 0.7rem;">
    <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:0.78rem;margin-bottom:0.3rem;">
      📈 Observability Stack
    </div>
    <ul style="margin:0;padding-left:1.1rem;font-size:0.7rem;line-height:1.75;">
      <li><strong>Prometheus</strong> — metrics collection &amp; custom metrics API</li>
      <li><strong>Grafana</strong> — dashboards &amp; visual alerting</li>
      <li><strong>RED Method</strong> — Rate · Errors · Duration as scaling signals</li>
      <li><strong>OpenTelemetry</strong> — vendor-neutral instrumentation standard</li>
    </ul>
  </div>

  <!-- Block 3: Scale-to-Zero -->
  <div class="metric-box" style="border:1px solid var(--accent-green,#16a34a);border-radius:8px;padding:0.55rem 0.7rem;">
    <div class="col-title" style="color:var(--accent-green,#16a34a);font-size:0.78rem;margin-bottom:0.3rem;">
      ⚡ Scale-to-Zero
    </div>
    <ul style="margin:0;padding-left:1.1rem;font-size:0.7rem;line-height:1.75;">
      <li><strong>Knative / Cloud Run / Lambda</strong> — zero idle cost</li>
      <li>No load → no instances → no cost</li>
      <li>Tradeoff: cold start latency must fit SLA</li>
      <li>Ideal for bursty, unpredictable workloads</li>
    </ul>
  </div>

  <!-- Block 4: FinOps & Resilience -->
  <div class="metric-box" style="border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:0.55rem 0.7rem;">
    <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:0.78rem;margin-bottom:0.3rem;">
      💸 FinOps &amp; Resilience
    </div>
    <ul style="margin:0;padding-left:1.1rem;font-size:0.7rem;line-height:1.75;">
      <li><strong>Spot / Preemptible Instances</strong> — up to 90% cheaper for scaled workers</li>
      <li>Scale up aggressively, scale down conservatively (cooldown)</li>
      <li><strong>Predictive Scaling</strong> — ML-based forecasting (AWS, GCP)</li>
      <li><strong>Chaos Engineering</strong> — verify autoscaling holds under real load</li>
    </ul>
  </div>

</div>

<div class="problem-insight" style="margin-top:0.5rem;">
  <span class="accent-comment">»</span>
  The <span class="accent-cyan">CNCF landscape</span> defines the de-facto standard —
  composable, observable, cost-aware autoscaling is the industry baseline.
  <span class="accent-comment">«</span>
</div>
