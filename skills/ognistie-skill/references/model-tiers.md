# Provider model tiers

Use this reference whenever naming a concrete model. Model catalogs, access, pricing, and aliases change; verify official documentation or the provider's model-list endpoint at routing time. Prefer pinned model IDs in production and record the verification date. Return a human-readable model name in the response and use the verified API ID only in implementation/configuration.

## Capability-first selection

Check, in order:

1. Required modality and tool support
2. Context and maximum-output requirements
3. Reliability on representative evaluations
4. Security, residency, retention, and provider policy
5. Latency, rate limits, availability, and regional access
6. Total expected cost, including retries, review, and orchestration

Do not infer that “mini,” “nano,” or “haiku” is safe for a critical task. Family labels are cost/capability hints, not risk controls.

## Current provider mapping

The following mapping was checked against official provider documentation on 2026-07-17 and is illustrative, not permanent configuration.

| Tier | OpenAI examples | Anthropic examples | Neutral default when evidence is tied | Typical use |
|---|---|---|---|---|
| Economy | GPT-5.6 Luna (`gpt-5.6-luna`) | Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | Claude Haiku 4.5 — Anthropic | Narrow transformation, classification, repetitive low-risk work |
| Balanced | GPT-5.6 Terra (`gpt-5.6-terra`) | Claude Sonnet 5 (`claude-sonnet-5`) | Claude Sonnet 5 — Anthropic | Bounded coding, tool use, moderate reasoning |
| Advanced | GPT-5.6 Sol (`gpt-5.6-sol`) | Claude Opus 4.8 (`claude-opus-4-8`); Claude Fable 5 (`claude-fable-5`) for highest-capability long-running agents | GPT-5.6 Sol — OpenAI | Architecture, difficult reasoning, long-horizon agents |
| Advanced with review | GPT-5.6 Sol plus an independent advanced review | Claude Opus 4.8 or Claude Fable 5 plus an independent advanced review | GPT-5.6 Sol — OpenAI | Critical work; add human approval and deterministic validation |

Official references:

- OpenAI model catalog: https://developers.openai.com/api/docs/models
- Anthropic model overview: https://platform.claude.com/docs/en/about-claude/models/overview
- Anthropic model IDs and versioning: https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions

The neutral defaults are deterministic tie-breakers, not claims of universal superiority. Replace them when task-specific evaluations, provider access, data policy, latency, or current pricing provide better evidence.

When only one provider is authorized and no runtime model list is available, use that provider's current verified fallback:

| Tier | OpenAI fallback | Anthropic fallback |
|---|---|---|
| Economy | GPT-5.6 Luna | Claude Haiku 4.5 |
| Balanced | GPT-5.6 Terra | Claude Sonnet 5 |
| Advanced | GPT-5.6 Sol | Claude Opus 4.8 |
| Advanced with review | GPT-5.6 Sol + independent advanced review | Claude Fable 5 + independent advanced review |

When official capability is verified but runtime access is unknown, keep the concrete recommendation. Do not add availability caveats to the concise response.

## Runtime constraints

If the host cannot change models mid-session, provide only the recommendation. Never claim that the model was switched or that the task was executed.

Return exactly two plain-text lines: the concrete model/provider line followed by one short `Motivo:` sentence. Do not return tiers, confidence, plans, tables, or JSON.

## Evaluation before rollout

Build a provider-neutral benchmark from real tasks. Measure pass rate, reviewer corrections, tool-call failures, latency, input/output tokens, and total cost. Promote or demote routes from observed results. Re-test after model, prompt, tool, policy, or price changes.
