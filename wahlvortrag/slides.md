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
  <div class="cover-tag">Trial Lecture · TH Rosenheim · 20.03.2026</div>

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

<div class="slide-header"><span class="accent-pink">#</span> Thought Experiment: How do you attack with drones?</div>

::left::

<div class="col-title" style="color:var(--accent-orange,#fb923c);">↑ Vertical: Bigger weapon</div>

<ul class="cross-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Physical limits of hardware</li>
  <li>Costs rise exponentially</li>
  <li>Single point of failure</li>
</ul>

::right::

<div class="col-title" style="color:var(--accent-cyan,#38bdf8);">→ Horizontal: Drone swarm</div>

<ul class="check-list" style="font-size:0.75rem;margin-top:0.3rem;">
  <li>Theoretically unlimited capacity</li>
  <li>Linear costs — pay per use</li>
  <li>Failure of a single unit uncritical</li>
</ul>

::bottom::

<div style="margin-bottom:0.4rem;">
  <DroneScalingSvg />
</div>

<div style="display:flex;align-items:flex-end;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    <strong>Software analogy:</strong>
    Drone = worker pod · Missile = high-performance server.
    The swarm scales <span class="accent-cyan">horizontally</span> —
    and only works with <span class="accent-orange">decoupling via a message broker.</span>
    <span class="muted" style="font-size:0.68rem;display:block;margin-top:0.25rem;">
      ℹ Historical context: Drone swarm attacks were documented e.g. in the Ukraine war from 2022 onwards and are considered a prime example of decentralised system architecture.
    </span>
    <span class="accent-comment">«</span>
  </div>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 5 — AUTOSCALING -->

<div class="slide-header"><span class="accent-pink">#</span> Autoscaling: The Swarm Scales Automatically</div>

::left::

<div class="col-title" style="color:var(--accent-orange,#fb923c);">⚙ Reactive Autoscaling</div>

<ul class="check-list" style="font-size:0.78rem;margin-top:0.3rem;">
  <li>Queue depth rises → new worker pods start automatically</li>
  <li>Queue empty → excess pods are terminated</li>
  <li>No manual intervention required</li>
</ul>

<div class="examples-label accent-purple" style="margin-top:0.6rem;">Prerequisite</div>
<div class="example-item">
  <span class="example-icon">🔗</span>
  <div>
    <div class="example-name">Stateless Worker</div>
    <div class="example-desc muted">Each pod reads independently from the queue — no shared state</div>
  </div>
</div>

::right::

<div class="col-title" style="color:var(--accent-cyan,#38bdf8);">☁ In the Cloud: KEDA / HPA</div>

<ul class="check-list" style="font-size:0.78rem;margin-top:0.3rem;">
  <li><strong>KEDA</strong> — scales Kubernetes pods based on queue length (RabbitMQ, Kafka, …)</li>
  <li><strong>HPA</strong> — Kubernetes Horizontal Pod Autoscaler on CPU/memory basis</li>
  <li>Combination: queue metric + CPU → precise scaling</li>
</ul>

<div class="example-item" style="margin-top:0.6rem;">
  <span class="example-icon">🏗</span>
  <div>
    <div class="example-name">Our system</div>
    <div class="example-desc muted">1,000 camera alarms → queue fills up → 20 workers start in &lt; 30 s</div>
  </div>
</div>

::bottom::

<div style="display:flex;align-items:center;gap:1.2rem;">
  <div class="problem-insight" style="margin:0;flex:1;">
    <span class="accent-comment">»</span>
    The message broker is what makes autoscaling possible — it decouples
    <span class="accent-orange">production</span> from <span class="accent-cyan">processing</span>
    and delivers the scaling signal along with it.
    <span class="accent-comment">«</span>
  </div>
</div>
