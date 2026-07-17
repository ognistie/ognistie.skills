# ognistie.skills

Skill portátil para recomendar o modelo de IA mais adequado antes da execução de uma tarefa.

## Como funciona

`ognistie-skill` analisa internamente a complexidade, o risco e o custo esperado. Em seguida, escolhe um modelo concreto da OpenAI ou Anthropic e responde somente em duas linhas:

```text
Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.
Motivo: Alteração visual moderada em interface existente; oferece boa qualidade de implementação com custo menor que modelos avançados.
```

A skill não executa a tarefa, não mostra relatório, tabela, tier, confiança, delegação ou plano.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
cd ognistie.skills
```

### OpenAI Codex

Copie `skills/ognistie-skill` para `~/.codex/skills/ognistie-skill`.

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.codex\skills\ognistie-skill"
```

macOS/Linux:

```bash
mkdir -p ~/.codex/skills
cp -R skills/ognistie-skill ~/.codex/skills/
```

Guia completo: [OpenAI](../platforms/openai/README.md).

### Anthropic Claude Code

Copie `skills/ognistie-skill` para `~/.claude/skills/ognistie-skill`.

PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.claude\skills\ognistie-skill"
```

macOS/Linux:

```bash
mkdir -p ~/.claude/skills
cp -R skills/ognistie-skill ~/.claude/skills/
```

Guia completo: [Anthropic](../platforms/anthropic/README.md).

Abra uma nova sessão do agente depois da instalação.

## Uso

Codex:

```text
$ognistie-skill Ajuste este componente visual e crie testes básicos.
```

Claude Code:

```text
/ognistie-skill Ajuste este componente visual e crie testes básicos.
```

Sem uma tarefa concreta, a resposta será somente:

```text
Envie a tarefa que deseja analisar.
```

## Validação

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

O pacote será criado em `dist/ognistie-skill.zip`.

## Contribuição e segurança

Consulte [CONTRIBUTING.md](../CONTRIBUTING.md) para contribuir e [SECURITY.md](../SECURITY.md) para relatar vulnerabilidades.

Licenciado sob a [MIT License](../LICENSE).
