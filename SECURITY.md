# Security policy

## Reporting a vulnerability

Do not disclose suspected vulnerabilities, credentials, or sensitive prompts in a public issue.

Use GitHub's private vulnerability reporting feature for this repository when available. Include:

- A concise description of the issue
- A safe reproduction or adversarial prompt
- Expected and observed behavior
- Potential impact
- Suggested mitigation, if known

Do not include live secrets or production data. Reports will be acknowledged and triaged as availability permits.

## Scope

Security-relevant behavior includes prompt injection resistance, provider-boundary violations, secret exposure, unsafe model downgrades for critical tasks, and packaging scripts that write outside their declared output directory.
