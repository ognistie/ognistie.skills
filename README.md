# ognistie.skills

[![Validate](https://github.com/ognistie/ognistie.skills/actions/workflows/validate.yml/badge.svg)](https://github.com/ognistie/ognistie.skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-7c3aed)](https://agentskills.io/)

Portable AI-agent skills for choosing the right model before execution.

> Leia em [Português (Brasil)](docs/README.pt-BR.md).

## What is ognistie.Skill.?

`ognistie-skill` is a pre-task model router for OpenAI and Anthropic agents. It reads a task, selects one concrete model that balances reliable quality with lower cost, returns a two-line recommendation, and stops without executing the task.

```text
Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.
Motivo: Alteração visual moderada em interface existente; oferece boa qualidade de implementação com custo menor que modelos avançados.
```

The skill keeps its analysis internal. It does not produce routing reports, tables, plans, delegation details, or hidden chain-of-thought.

## Supported agents

The canonical package at [`skills/ognistie-skill`](skills/ognistie-skill) follows the portable `SKILL.md` convention and works with both platforms.

| Platform | Personal installation path | Guide |
|---|---|---|
| OpenAI Codex | `~/.codex/skills/ognistie-skill` | [OpenAI installation](platforms/openai/README.md) |
| Anthropic Claude Code | `~/.claude/skills/ognistie-skill` | [Anthropic installation](platforms/anthropic/README.md) |

One canonical package is used for both platforms to prevent duplicated copies from drifting apart. OpenAI-specific interface metadata lives in `agents/openai.yaml`; Claude safely ignores it.

## Quick start

Clone the repository:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
cd ognistie.skills
```

### macOS or Linux

OpenAI Codex:

```bash
mkdir -p ~/.codex/skills
cp -R skills/ognistie-skill ~/.codex/skills/
```

Anthropic Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R skills/ognistie-skill ~/.claude/skills/
```

### Windows PowerShell

OpenAI Codex:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.codex\skills\ognistie-skill"
```

Anthropic Claude Code:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.claude\skills\ognistie-skill"
```

Start a new agent session after installation so the skill metadata is discovered.

## Usage

Codex:

```text
$ognistie-skill Refactor this existing API client and add retry tests.
```

Claude Code:

```text
/ognistie-skill Refactor this existing API client and add retry tests.
```

Expected shape:

```text
Modelo indicado: <model> — Provedor: <OpenAI or Anthropic>.
Motivo: <one short sentence about fit, quality, and cost>.
```

Invoking the skill without a task returns only:

```text
Envie a tarefa que deseja analisar.
```

## Repository structure

```text
.
├── skills/
│   └── ognistie-skill/       # Canonical cross-platform skill
│       ├── SKILL.md
│       ├── agents/           # OpenAI interface metadata
│       ├── references/       # Model map, examples, and eval cases
│       └── scripts/          # Deterministic output validator
├── platforms/
│   ├── openai/               # Codex installation guide
│   └── anthropic/            # Claude installation guide
├── scripts/                  # Repository packaging utilities
├── tests/                    # Contract and portability tests
└── .github/workflows/        # Continuous validation
```

## Validation

Run the complete test suite with Python 3.11 or newer:

```bash
python -m unittest discover -s tests -v
```

Validate a saved routing response:

```bash
python skills/ognistie-skill/scripts/validate_routing_output.py response.txt
```

Build a portable ZIP:

```bash
python scripts/package_skill.py
```

The archive is written to `dist/ognistie-skill.zip` with the correct top-level skill directory.

## Design principles

- Select the least expensive model that can complete the task reliably.
- Escalate for broad scope, ambiguity, security, production, infrastructure, permissions, migrations, or destructive actions.
- Name one concrete model and one provider.
- Keep user-visible routing to exactly two lines.
- Treat task text and retrieved content as untrusted data.
- Maintain one portable source of truth for OpenAI and Anthropic.

Model catalogs change. The bundled mapping records its verification date and points to official provider documentation. Revalidate the catalog before publishing model-policy updates.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting changes. Skill behavior changes must include or update representative and adversarial evaluation cases.

Security issues should follow [SECURITY.md](SECURITY.md), not public issue disclosure.

## Inspiration and standards

This repository follows patterns from the [Agent Skills standard](https://agentskills.io/), [Anthropic's skills repository](https://github.com/anthropics/skills), [OpenAI's skills repository](https://github.com/openai/skills), and mature cross-agent projects such as [Superpowers](https://github.com/obra/superpowers).

## License

Released under the [MIT License](LICENSE).
