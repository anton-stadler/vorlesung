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
layout: two-cols-header-with-footer
---

<!-- SLIDE 2 — SCALING STRATEGIES -->

<div class="slide-header"><span class="accent-pink">#</span> Scaling Strategies: Vertical vs. Horizontal</div>

::left::

<div class="col-title check">↑ Vertical Scaling (Scale-Up)</div>

<ul class="check-list">
  <li>Buy a bigger machine — more CPU, RAM, NVMe</li>
  <li>No architecture change needed</li>
  <li>Low latency between components</li>
</ul>

<ul class="cross-list" style="margin-top: 0.5rem;">
  <li>Physical hardware limits</li>
  <li>Exponential cost curve</li>
  <li>Single point of failure</li>
</ul>

<div class="examples-label accent-purple">When useful</div>

<div class="example-item">
  <span class="example-icon">🏛</span>
  <div>
    <div class="example-name">Monolithic apps</div>
    <div class="example-desc muted">No distributed state to coordinate</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">⏱</span>
  <div>
    <div class="example-name">Quick short-term fix</div>
    <div class="example-desc muted">Buys time — doesn't solve the problem</div>
  </div>
</div>

::right::

<div class="col-title check">→ Horizontal Scaling (Scale-Out)</div>

<ul class="check-list">
  <li>More machines — load distributed</li>
  <li>Theoretically unlimited capacity</li>
  <li>High availability, commodity hardware</li>
</ul>

<ul class="cross-list" style="margin-top: 0.5rem;">
  <li>Requires stateless workers</li>
  <li>Needs external coordination</li>
  <li><strong>No tight coupling allowed</strong></li>
</ul>

<div class="examples-label accent-purple">Key prerequisite</div>

<div class="example-item">
  <span class="example-icon">🔗</span>
  <div>
    <div class="example-name">Decoupled producers &amp; consumers</div>
    <div class="example-desc muted">Producer must not know consumer address</div>
  </div>
</div>

::bottom::

<div class="problem-insight">
  <span class="accent-comment">»</span>
  What prevents us from simply starting <span class="accent-orange">100 workers</span>?
  → <span class="accent-red">Tight coupling.</span>
  If producer points directly to consumer, every worker must know every address.
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 3 — THE PROBLEM: DIRECT COUPLING -->

<div class="slide-header">
  <span class="accent-pink">#</span> The Problem: Direct Coupling
</div>

<div class="scenario-label">
  <span class="accent-comment">// Scenario:</span> <span class="accent-cyan">10,000 cameras detect threats simultaneously</span>
</div>

<div class="problem-layout">
  <div class="db-box">
    <div class="db-icon">📷</div>
    <div class="db-name accent-cyan">Edge Camera</div>
    <div class="db-field">
      confidence = <span class="accent-green">0.97</span>
    </div>
    <div class="db-field" style="margin-top: 0.3rem; font-size: 0.7rem;">
      → <span class="accent-orange">HTTP POST</span> worker:8080
    </div>
  </div>

  <div class="problem-questions">
    <ProblemBox>What if the worker crashes?</ProblemBox>
    <ProblemBox>50 alarms arrive in 1 second?</ProblemBox>
    <ProblemBox>How to add more workers?</ProblemBox>
  </div>
</div>

<div class="problem-insight">
  <span class="accent-comment">»</span>
  Tight coupling is the <span class="accent-orange">actual problem</span> —
  not the <span class="accent-red">load itself.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 4 — THE SOLUTION: PRODUCER · BROKER · CONSUMER -->

<div class="slide-header">
  <span class="accent-pink">#</span> The Solution: Producer · Broker · Consumer
</div>

<div style="display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 0.8rem; align-items: center; margin: 1rem 0;">
  <div class="db-box" style="text-align: center;">
    <div class="db-icon">📷</div>
    <div class="db-name accent-cyan">Producer</div>
    <div class="db-field">Edge Camera</div>
    <div class="db-field muted" style="font-size: 0.65rem;">MQTT publish</div>
  </div>
  <div style="font-size: 1.4rem; color: var(--accent-pink);">→</div>
  <div class="db-box" style="text-align: center; border-color: var(--accent-orange);">
    <div class="db-icon">📮</div>
    <div class="db-name accent-orange">Broker</div>
    <div class="db-field">MQTT / RabbitMQ</div>
    <div class="db-field muted" style="font-size: 0.65rem;">queue &amp; fan-out</div>
  </div>
  <div style="font-size: 1.4rem; color: var(--accent-pink);">→</div>
  <div class="db-box" style="text-align: center;">
    <div class="db-icon">⚙</div>
    <div class="db-name accent-purple">Consumer</div>
    <div class="db-field">Verification Worker</div>
    <div class="db-field muted" style="font-size: 0.65rem;">Kubernetes pod</div>
  </div>
</div>

<div class="cards-grid" style="margin-top: 0.8rem;">
  <InfoCard title="Space" icon="📍" color="cyan">
    <template #subtitle>Decoupling in Space</template>
    <ul>
      <li>Producer doesn't know consumer address</li>
      <li>Consumer doesn't know who produced</li>
      <li>Both can be replaced independently</li>
    </ul>
  </InfoCard>

  <InfoCard title="Time" icon="⏱" color="purple">
    <template #subtitle>Decoupling in Time</template>
    <ul>
      <li>Producer doesn't wait for consumer</li>
      <li>Consumer processes at own pace</li>
      <li>Messages persist during downtime</li>
    </ul>
  </InfoCard>

  <InfoCard title="Number" icon="✕" color="orange">
    <template #subtitle>Decoupling in Number</template>
    <ul>
      <li>Any number of consumers can subscribe</li>
      <li>Scale workers up/down dynamically</li>
      <li>Fan-out: one message → many consumers</li>
    </ul>
  </InfoCard>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 5 — KEDA: AUTO-SCALING -->

<div class="slide-header">
  <span class="accent-pink">#</span> KEDA: Kubernetes Event-Driven Autoscaling
</div>
<div class="scenario-label">
  <span class="accent-comment">// Scaling metric:</span> <span class="accent-cyan">queue depth — KEDA polls the RabbitMQ queue and adjusts pod count</span>
</div>
<div style="background: var(--slide-bg-alt, #EFEFEA); border: 1px solid var(--slide-border, #CCCCCC); border-radius: 6px; padding: 0.5rem 1.2rem; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; margin: 0.5rem 0 0.7rem;">
  <div class="muted" style="font-size: 0.65rem; margin-bottom: 0.2rem;">// KEDA scaling formula</div>
  <div><span class="accent-orange">target_replicas</span> = ⌈ <span class="accent-cyan">queue_length</span> / <span class="accent-purple">target_msgs_per_pod</span> ⌉</div>
</div>
<div class="cards-grid">
  <InfoCard title="Monitors" icon="👁" color="cyan">
    <template #subtitle>Queue Depth Polling</template>
    <ul>
      <li>Polls RabbitMQ metrics continuously</li>
      <li>Configurable polling interval</li>
      <li>Zero changes needed on workers</li>
    </ul>
  </InfoCard>

  <InfoCard title="Scales 1 → n" icon="⚡" color="purple">
    <template #subtitle>Automatic Pod Management</template>
    <ul>
      <li>Queue grows → new pods scheduled</li>
      <li>Queue empty → pods scale to 0</li>
      <li>Reaction time: <strong>&lt;30 seconds</strong></li>
    </ul>
  </InfoCard>

  <InfoCard title="Cost-Efficient" icon="💰" color="orange">
    <template #subtitle>Pay Per Use</template>
    <ul>
      <li>🌙 Night at airport: 1 worker</li>
      <li>✈ Morning rush: 50+ workers</li>
      <li>No pre-provisioning needed</li>
    </ul>
  </InfoCard>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 6 — LIVE DEMO: SCALING SIMULATOR -->

<div class="slide-header"><span class="accent-pink">#</span> Live Demo: Scaling Simulator</div>

<div style="flex:1;min-height:0;display:flex;flex-direction:column;">
  <ScalingDemo />
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 7 — CASE STUDY: GUN DETECTION SYSTEM -->

<div class="slide-header"><span class="accent-pink">#</span> Case Study: Gun Detection System</div>

::left::

<div class="scenario-label">
  <span class="accent-comment">// Architecture:</span> <span class="accent-cyan">Edge → Broker → Cloud</span>
</div>
<div class="example-item">
  <span class="example-icon" style="background: var(--accent-cyan); color: white; padding: 0.15rem 0.4rem; border-radius: 4px; font-style: normal; font-size: 0.65rem; min-width: auto;">EDGE</span>
  <div>
    <div class="example-name">IP Camera → CNN (C++) → confidence score</div>
    <div class="example-desc muted">if confidence &gt; θ → publish ~1 KB JSON alarm event</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon" style="background: var(--accent-orange); color: white; padding: 0.15rem 0.4rem; border-radius: 4px; font-style: normal; font-size: 0.65rem; min-width: auto;">BROKER</span>
  <div>
    <div class="example-name">MQTT (edge→cloud) · RabbitMQ (cloud fan-out)</div>
    <div class="example-desc muted">KEDA monitors queue depth continuously</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon" style="background: var(--accent-purple); color: white; padding: 0.15rem 0.4rem; border-radius: 4px; font-style: normal; font-size: 0.65rem; min-width: auto;">CLOUD</span>
  <div>
    <div class="example-name">Kubernetes workers · GenAI verification model</div>
    <div class="example-desc muted">Adaptive threshold θ fed back to edge</div>
  </div>
</div>

::right::

<div class="examples-label accent-purple">Measurement Data</div>
<div class="example-item">
  <span class="example-icon">🟢</span>
  <div>
    <div class="example-name"><span class="accent-green">&gt;99%</span> frames filtered on edge</div>
    <div class="example-desc muted">Only alarms reach the cloud</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">📉</span>
  <div>
    <div class="example-name"><span class="accent-cyan">200:1</span> bandwidth reduction</div>
    <div class="example-desc muted">~1 KB JSON vs. ~200 KB raw frame</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">🔒</span>
  <div>
    <div class="example-name"><span class="accent-purple">99.99%</span> SLA</div>
    <div class="example-desc muted">Via horizontal redundancy</div>
  </div>
</div>
<div class="example-item">
  <span class="example-icon">⚡</span>
  <div>
    <div class="example-name"><span class="accent-orange">&lt;30 s</span> auto-scaling reaction</div>
    <div class="example-desc muted">1 → 50+ workers automatically</div>
  </div>
</div>

::bottom::

<div class="problem-insight">
  <span class="accent-comment">»</span>
  The edge acts as an <span class="accent-orange">intelligent filter</span> — making horizontal cloud scaling <span class="accent-green">economically viable.</span>
  Without this filter, cloud costs would be <span class="accent-red">200× higher.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: two-cols-header-with-footer
---

<!-- SLIDE 8 — TRADE-OFFS -->

<div class="slide-header"><span class="accent-pink">#</span> Trade-offs &amp; Scientific Classification</div>

::left::

<div class="col-title" style="color: var(--accent-cyan);">⚖ Latency vs. Throughput</div>
<div style="font-size: 0.75rem; margin-bottom: 0.8rem;">
  Broker adds <span class="accent-orange">5–50 ms</span> overhead (serialization + network hop).<br>
  <span class="muted">Acceptable for alarm verification. Unacceptable for surgical robotics or autonomous driving.</span><br>
  <strong>Positioning:</strong> <span class="accent-green">CNN on edge handles real-time — broker overhead is irrelevant.</span>
</div>

<div class="col-title" style="color: var(--accent-purple);">📬 At-Least-Once vs. Exactly-Once</div>
<div style="font-size: 0.75rem;">
  <span class="accent-orange">At-least-once</span>: simpler, faster — but may process same message twice.<br>
  <span class="accent-red">Exactly-once</span>: no duplicates — but expensive (2-phase commit, reduced availability).<br>
  <strong>In practice:</strong> <span class="accent-green">at-least-once + idempotency</span> is almost always the right trade-off.<br>
  <span class="muted" style="font-size: 0.68rem;">→ CAP theorem (Brewer 2000): exactly-once sacrifices availability.</span>
</div>

::right::

<div class="col-title" style="color: var(--accent-orange);">🔀 Ordering vs. Parallelism</div>
<div style="font-size: 0.75rem; margin-bottom: 0.8rem;">
  Strict FIFO prevents parallel processing by multiple consumers.<br>
  <strong>Solution — partitioning:</strong> order within partition, parallelism across partitions.<br>
  <span class="accent-green">Partition by camera ID</span>: ordered per stream + full horizontal scalability across streams.
</div>

<div class="col-title" style="color: var(--accent-red);">🚫 When NOT to use a broker</div>
<ul class="cross-list" style="font-size: 0.75rem;">
  <li>Very low load (&lt;10 req/s) — overhead exceeds benefit</li>
  <li>Ultra-low-latency (&lt;5 ms) — use direct gRPC instead</li>
  <li>Simple 1:1 communication without scaling need</li>
</ul>

::bottom::

<div class="problem-insight">
  <span class="accent-comment">»</span>
  A message broker is not a <span class="accent-orange">silver bullet.</span>
  It is the right tool when you need to <span class="accent-cyan">decouple producers from consumers at scale</span> —
  and <span class="accent-red">wrong when you don't.</span>
  <span class="accent-comment">«</span>
</div>

---
layout: default-with-footer
---

<!-- SLIDE 9 — RESEARCH OUTLOOK -->

<div class="slide-header">
  <span class="accent-pink">#</span> Research Outlook &amp; Open Questions
</div>

<div class="cards-grid">
  <InfoCard title="Adaptive Scaling" icon="🔮" color="cyan">
    <template #subtitle>Proactive Auto-Scaling</template>
    <ul>
      <li>Current state: KEDA scales <strong>reactively</strong></li>
      <li>Open question: Can we scale <strong>before</strong> the queue fills?</li>
      <li>Approach: LSTM / Transformer on queue depth + camera load patterns</li>
      <li>Goal: Eliminate latency spikes during load peaks</li>
    </ul>
  </InfoCard>

  <InfoCard title="Federated Brokers" icon="🌐" color="purple">
    <template #subtitle>Global Edge Networks</template>
    <ul>
      <li>Problem: Central broker = single point of failure</li>
      <li>Approach: Hierarchical broker topology</li>
      <li>Local brokers at edge · global coordination broker</li>
      <li>Open: Consistency across geo-distributed brokers without violating CAP</li>
    </ul>
  </InfoCard>

  <InfoCard title="Federated Learning" icon="🧠" color="orange">
    <template #subtitle>Privacy-Preserving AI via Broker</template>
    <ul>
      <li>Idea: Edge devices train locally, send only gradients</li>
      <li>No sensitive video data leaves the building</li>
      <li>Broker aggregates model updates horizontally</li>
      <li>Open: Gradient aggregation at scale without bottleneck</li>
    </ul>
  </InfoCard>
</div>

<div class="problem-insight" style="margin-top: 0.8rem;">
  <span class="accent-comment">»</span>
  We've seen that message-based architecture makes horizontal scaling <span class="accent-green">possible.</span>
  The next question: how to scale <span class="accent-cyan">intelligently</span> —
  <span class="accent-orange">before the system feels the pressure.</span>
  <span class="accent-comment">«</span>
</div>
