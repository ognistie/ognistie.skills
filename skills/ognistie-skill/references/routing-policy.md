# Routing policy

Apply the quality floor first and cost second. A cheaper model is acceptable only when it can complete the task reliably without likely retries or advanced review.

## Mandatory escalation

Select `advanced` when any condition applies:

- Security, authentication, authorization, credentials, privacy, compliance, or formal review
- Production, infrastructure, deployment, permissions, destructive operations, migrations, or material data-loss risk
- Broad architecture, cross-service design, difficult diagnosis, large refactors, or unclear blast radius
- High ambiguity, conflicting requirements, long-horizon agentic work, or many dependent steps
- Failure could cause financial, legal, safety, availability, or reputational harm

Select the strongest suitable advanced candidate and require independent review internally when the task combines critical impact with high ambiguity, irreversible effects, or sustained autonomous execution.

## Economy

Use `economy` only when every condition is true:

- The request is narrow, explicit, local, repetitive, and reversible.
- Acceptance criteria are clear.
- No critical-risk escalation applies.
- Limited reasoning, context, tools, and coordination are required.
- A retry would be inexpensive and harmless.

Examples: typo correction, short classification, formatting, simple extraction, small deterministic transformation.

## Balanced

Use `balanced` for bounded work that exceeds economy but triggers no advanced condition:

- Normal feature implementation or debugging
- Moderate UI work
- Bounded API integration, CRUD, or test creation
- Small refactor across a known set of files
- Tool use and multi-step reasoning with a clear scope

## Provider and model selection

1. Keep the current or explicitly authorized provider for sensitive tasks.
2. Remove candidates lacking required modality, tools, context, output capacity, regional availability, or data-policy compatibility.
3. Prefer task-specific evaluation evidence when available.
4. Estimate total expected cost: initial call + likely retries + required review.
5. Use catalog price only as the final comparison among candidates that meet the quality floor.
6. If a dated promotional price has expired, use the catalog's standard price until official documentation is checked.
7. If evidence is tied, prefer the current provider to avoid data transfer and operational friction.
8. If the tier remains uncertain, choose the stronger tier.

## Task-fit guidance

- Prefer economy models for high-volume, low-risk transformations.
- Prefer balanced models for bounded coding and normal tool use.
- Prefer advanced models for complex professional reasoning and critical reviews.
- Prefer the highest-capability long-running-agent model only when the task genuinely requires sustained autonomous work; do not use it for ordinary advanced tasks.

## Cost interpretation

Do not claim a precise saving without measured input/output tokens and current prices. Model routing normally reduces monetary cost per token, not the number of tokens. The routing step itself adds overhead and can make very small tasks more expensive.
