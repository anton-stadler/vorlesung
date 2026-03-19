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
routeAlias: cover

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
routeAlias: fire-detection
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
layout: default-with-footer
routeAlias: broker
---

<!-- SLIDE 3 — MESSAGE BROKER -->

<div class="slide-header"><span class="accent-pink">#</span> Message Broker: Decoupling Strategy</div>

<div style="display:grid;grid-template-rows:auto 1fr auto auto;gap:0.7rem;flex:1;min-height:0;">

  <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:0;">
    <BrokerDiagramSvg :brokerOnly="true" />
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">
    <div v-click="1" style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:0.9rem 1.2rem;display:flex;flex-direction:column;gap:0.3rem;">
      <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:1rem;">📬 Buffering</div>
      <div class="muted" style="font-size:0.85rem;line-height:1.6;">Burst of alarms? Queue absorbs the load — no message is lost.</div>
    </div>
    <div v-click="1" style="border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:0.9rem 1.2rem;display:flex;flex-direction:column;gap:0.3rem;">
      <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:1rem;">↔ Decoupling</div>
      <div class="muted" style="font-size:0.85rem;line-height:1.6;">Camera doesn't know workers — add or remove them freely.</div>
    </div>
    <div v-click="1" style="border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:0.9rem 1.2rem;display:flex;flex-direction:column;gap:0.3rem;">
      <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:1rem;">⚡ Scalability</div>
      <div class="muted" style="font-size:0.85rem;line-height:1.6;">Spin up any number of workers — broker distributes the work.</div>
    </div>
  </div>

  <div v-click="2" class="problem-insight" style="margin:0;">
    <span class="accent-comment">»</span>
    The broker decouples <span class="accent-orange">who sends</span> from <span class="accent-cyan">who processes</span> — enabling horizontal scaling.
    <span class="accent-comment">«</span>
  </div>

</div>

---
layout: default-with-footer
routeAlias: scaling
---

<!-- SLIDE 4 — SCALING: DRONE ANALOGY -->

<div class="slide-header"><span class="accent-pink">#</span> One big unit vs. many small ones</div>

<div style="display:grid;grid-template-rows:auto 1fr;gap:0.8rem;flex:1;min-height:0;">

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
    <div style="border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:1rem 1.4rem;">
      <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:1.05rem;">↑ Vertical Scaling</div>
      <ul class="check-list" style="font-size:0.95rem;margin-top:0.8rem;line-height:2.1;">
        <li>Low latency, simple model</li>
      </ul>
      <ul class="cross-list" style="font-size:0.95rem;margin-top:0.3rem;line-height:2.1;">
        <li>Hardware limits</li>
        <li>Cost scales superlinearly</li>
      </ul>
    </div>
    <div style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:1rem 1.4rem;">
      <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:1.05rem;">→ Horizontal Scaling</div>
      <ul class="check-list" style="font-size:0.95rem;margin-top:0.8rem;line-height:2.1;">
        <li>Scales to any load</li>
        <li>Linear cost — pay per use</li>
      </ul>
      <ul class="cross-list" style="font-size:0.95rem;margin-top:0.3rem;line-height:2.1;">
        <li>Network overhead &amp; coordination</li>
      </ul>
    </div>
  </div>

  <div style="display:flex;flex-direction:column;justify-content:center;min-height:0;gap:0.4rem;">
    <div style="display:flex;justify-content:center;align-items:center;gap:1.5rem;flex:1;min-height:0;">
      <div style="display:flex;flex-direction:column;gap:0.5rem;align-items:center;">
        <span class="badge badge-orange" style="font-size:0.72rem;width:8rem;text-align:center;">scale up ↑</span>
        <span class="badge badge-orange" style="font-size:0.72rem;width:8rem;text-align:center;">scale down ↓</span>
      </div>
      <img src="/images/Scaling-Options.png" style="max-height:11rem;" />
      <div style="display:flex;flex-direction:column;gap:0.5rem;align-items:center;">
        <span class="badge badge-cyan" style="font-size:0.72rem;width:8rem;text-align:center;">scale out →</span>
        <span class="badge badge-cyan" style="font-size:0.72rem;width:8rem;text-align:center;">scale in ←</span>
      </div>
    </div>
    <div class="problem-insight" style="margin-top:0.2rem;">
      <span class="accent-comment">»</span>
      Swarm scales <span class="accent-cyan">horizontally</span> — needs a <span class="accent-orange">message broker.</span>
      <span class="accent-comment">«</span>
    </div>
  </div>

</div>

---
layout: default-with-footer
routeAlias: autoscaling
---

<!-- SLIDE 5 — AUTOSCALING -->

<div class="slide-header"><span class="accent-pink">#</span> Autoscaling — let metrics decide.</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;flex:1;min-height:0;">

  <div v-click style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:1.2rem 1.4rem;display:flex;flex-direction:column;gap:0.5rem;">
    <div style="font-size:2rem;">📬</div>
    <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:1.05rem;">Queue</div>
    <div style="font-size:0.75rem;color:var(--slide-muted,#64748B);font-style:italic;">KEDA</div>
    <div class="muted" style="font-size:0.88rem;line-height:1.7;flex:1;">
      Scale out when the queue grows.<br>
      Scale in when it empties.<br><br>
      <span style="color:var(--accent-cyan,#38bdf8);">→ Best for bursty workloads.</span>
    </div>
  </div>

  <div v-click style="border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:1.2rem 1.4rem;display:flex;flex-direction:column;gap:0.5rem;">
    <div style="font-size:2rem;">🔥</div>
    <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:1.05rem;">Load / CPU</div>
    <div style="font-size:0.75rem;color:var(--slide-muted,#64748B);font-style:italic;">HPA</div>
    <div class="muted" style="font-size:0.88rem;line-height:1.7;flex:1;">
      Scale out when workers are hot.<br>
      Scale in when utilization drops.<br><br>
      <span style="color:var(--accent-orange,#fb923c);">→ Best for CPU-bound tasks.</span>
    </div>
  </div>

  <div v-click style="border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:1.2rem 1.4rem;display:flex;flex-direction:column;gap:0.5rem;">
    <div style="font-size:2rem;">⏱</div>
    <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:1.05rem;">Latency</div>
    <div style="font-size:0.75rem;color:var(--slide-muted,#64748B);font-style:italic;">deadline-driven</div>
    <div class="muted" style="font-size:0.88rem;line-height:1.7;flex:1;">
      Scale out when wait time exceeds the response-time limit.<br>
      Scale in when latency relaxes.<br><br>
      <span style="color:var(--accent-purple,#bd93f9);">→ Best for time-critical systems.</span>
    </div>
  </div>

</div>

<div v-click class="problem-insight" style="margin-top:0.8rem;">
  <span class="accent-comment">»</span>
  The broker decouples senders from workers —
  metrics tell <span class="accent-cyan">when</span> to scale, platform handles <span class="accent-orange">how.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
routeAlias: tradeoffs
---

<!-- TRADEOFF SLIDE -->

<div class="slide-header"><span class="accent-pink">#</span> Scale smart — three competing forces.</div>

<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;flex:1;min-height:0;">

  <div v-click style="border:1px solid var(--accent-red,#f87171);border-radius:8px;padding:1.6rem 1.4rem;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.8rem;">
    <div style="font-size:2.8rem;">🛡</div>
    <div class="col-title" style="color:var(--accent-red,#f87171);font-size:1.1rem;text-align:center;">Reliability</div>
    <div class="muted" style="font-size:0.85rem;text-align:center;line-height:1.7;">No message loss.<br>Every alarm must arrive.</div>
  </div>

  <div v-click style="border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:1.6rem 1.4rem;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.8rem;">
    <div style="font-size:2.8rem;">⚡</div>
    <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:1.1rem;text-align:center;">Latency</div>
    <div class="muted" style="font-size:0.85rem;text-align:center;line-height:1.7;">Low response time.<br>Alarms processed within 2 s.</div>
  </div>

  <div v-click style="border:1px solid var(--accent-green,#4ade80);border-radius:8px;padding:1.6rem 1.4rem;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0.8rem;">
    <div style="font-size:2.8rem;">💰</div>
    <div class="col-title" style="color:var(--accent-green,#16a34a);font-size:1.1rem;text-align:center;">Cost</div>
    <div class="muted" style="font-size:0.85rem;text-align:center;line-height:1.7;">Pay per use.<br>No idle workers at night.</div>
  </div>

</div>

<div v-click class="problem-insight" style="margin-top:0.8rem;">
  <span class="accent-comment">»</span>
  Too many workers → <span class="accent-orange">cost explodes.</span>
  Too few → <span class="accent-red">alarms are lost or slow.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
routeAlias: takeaways
---

<!-- SLIDE — TAKEAWAYS -->

<div class="slide-header"><span class="accent-pink">#</span> What we learned today.</div>

<div style="display:grid;grid-template-rows:repeat(4,1fr);gap:0.55rem;flex:1;min-height:0;margin-top:0.4rem;">

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-cyan,#38bdf8);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">🔥</div>
    <div>
      <div class="col-title" style="color:var(--accent-cyan,#38bdf8);font-size:0.95rem;">Hybrid Edge–Cloud</div>
      <div class="muted" style="font-size:0.8rem;">Fast local inference + powerful cloud models — best of both worlds.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-orange,#fb923c);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">📨</div>
    <div>
      <div class="col-title" style="color:var(--accent-orange,#fb923c);font-size:0.95rem;">Message Broker = Decoupling</div>
      <div class="muted" style="font-size:0.8rem;">Producers and consumers never talk directly — the broker absorbs bursts.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-purple,#bd93f9);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">↔</div>
    <div>
      <div class="col-title" style="color:var(--accent-purple,#bd93f9);font-size:0.95rem;">Horizontal over Vertical</div>
      <div class="muted" style="font-size:0.8rem;">Many small workers scale linearly — one big machine hits a ceiling.</div>
    </div>
  </div>

  <div v-click style="display:flex;align-items:center;gap:1rem;border:1px solid var(--accent-green,#4ade80);border-radius:8px;padding:0.55rem 1.2rem;">
    <div style="font-size:1.5rem;min-width:2rem;text-align:center;">📊</div>
    <div>
      <div class="col-title" style="color:var(--accent-green,#4ade80);font-size:0.95rem;">Autoscaling — metrics decide</div>
      <div class="muted" style="font-size:0.8rem;">Queue depth, CPU, latency — let the platform scale for you.</div>
    </div>
  </div>

</div>

---
layout: default
routeAlias: thanks
---

<!-- SLIDE — THANKS -->

<div class="cover-wrap">
  <h1 class="cover-title" style="font-size:2.2rem;">Thank you for your<br>
    <span class="accent-cyan">attention!</span>
  </h1>
  <div class="cover-meta" style="margin-top:1.5rem;">
    <div class="cover-author">Dr.-Ing. Anton Stadler</div>
  </div>
</div>

---
layout: default
backup: true
routeAlias: backup
---

<!-- BACKUP — INDUSTRY STANDARDS -->

<div class="slide-header">
  <span class="accent-cyan">#</span> Further thoughts &amp; industry standards.
  <span class="muted text-sm" style="font-size:0.65em; margin-left:0.5rem;">BACKUP</span>
</div>

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
