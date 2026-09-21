# Model routing policy

Cowork never names a concrete model. It sends a **role alias** — `planning` or
`coding` — and the gateway decides which Bedrock model actually serves the
request. This is the "Model Router / Routing Policy" box in the System
Architecture diagram.

The policy lives in `litellm-config.yaml` rather than in Cowork, for one
structural reason: `LLMClient` fixes `planning_model` and `coding_model` at
construction time (`anton/core/llm/client.py`), so Cowork cannot re-decide per
request. The gateway can, because it sees the actual payload — token count,
tools, attachments.

## Three layers

Evaluated cheapest-signal-first, so the decision costs well under a millisecond
and never requires a model call of its own. Routing should remove more latency
than it adds.

### 1. Capability — can this model serve the request at all?

A hard filter, not a preference. `enable_pre_call_checks` drops any deployment
whose context window cannot hold the request, *before* spending a call to
discover that. When nothing in the tier fits, `context_window_fallbacks`
escalates to a roomier tier instead of returning an error:

```
bulk (128k)  →  coding (300k)  →  planning (200k)
```

Verified: a 157,055-token request to `bulk` was served by Nova Pro, not
rejected.

### 2. Quality tier — which class of model is appropriate?

The alias itself. Tiers are **quality-homogeneous**, and this is the load-bearing
design decision: LiteLLM's cost routing always picks the cheapest member of a
group, so putting Opus and Haiku in one group would silently downgrade every
request to Haiku. A tier may only contain models that are all acceptable for
that tier's work — cost then breaks a tie between genuine peers rather than
choosing the quality level.

| Alias | Members | For |
|---|---|---|
| `planning` | Sonnet 4.5, Opus 4.5 | user-facing reasoning loop, tool calls, vision |
| `coding` | Nova Pro, Haiku 4.5 | skill and code execution |
| `bulk` | gpt-oss-120b, qwen3-32b, qwen3-coder-30b | high-volume, low-stakes work |

### 3. Cost / latency — which peer within the tier?

- **`cost-based-routing`** (default) where members differ in price. `planning`
  picks Sonnet over Opus; `coding` picks Nova Pro over Haiku.
- **`latency-based-routing`** for `bulk`, whose members are priced identically
  ($0.15/$0.60) — cost cannot discriminate, so speed is what is left. Observed
  over 12 requests: qwen3-32b 6, qwen3-coder 4, gpt-oss-120b 2.

Per-token prices are declared explicitly in the config. LiteLLM's built-in cost
map does not cover the open-weight Bedrock models and silently assumes
**$1/token** for anything unlisted — which would make cost routing pick
essentially at random.

## Failure handling

Different failures need different responses; treating them all as "retry and
fall back" is the common mistake.

- **Context window exceeded** → `context_window_fallbacks` (a capacity decision)
- **5xx / throttling** → `fallbacks` to a peer or cheaper tier
- **Repeated failures** → circuit breaker: `allowed_fails: 3`, then a
  `cooldown_time: 30` during which that deployment is skipped, instead of
  letting every request time out against it

## Escape hatch

Every model is also registered under its own single-deployment alias
(`claude-opus-4-5`, `qwen3-32b`, …). Selecting one of those in Settings pins the
model and bypasses the policy entirely. Leave the model setting **blank** for
routing to apply — a pinned value wins.

## What this is not

No semantic or predictive routing. Both were considered and deliberately left
out:

- **Semantic routing** (embed the prompt, route by meaning) adds ~5ms and needs
  a similarity threshold that misroutes ambiguous traffic when wrong.
- **Predictive routing** (RouteLLM-style learned policies) needs labelled
  preference data and a stable query distribution, and degrades under
  distribution shift.

The standard advice is to start rule-based, because it is sub-millisecond and
debuggable, and to reach for a learned router only once a simpler one
demonstrably falls short. Add a semantic cache in front before improving model
selection — a cache hit skips routing and the model call entirely.

## Changing the policy

Edit `litellm-config.yaml`, then:

```bash
docker compose -f deploy/local/docker-compose.yml up -d --force-recreate
```

Confirm which deployment served a request by mapping the `x-litellm-model-id`
response header through `GET /model/info`.
