# ognistie.skills

## O que é

`ognistie-skill` analisa uma tarefa antes da execução e recomenda um modelo da OpenAI ou Anthropic, equilibrando qualidade e custo.

A resposta é curta e direta:

```text
Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.
Motivo: Alteração visual moderada oferece boa qualidade com custo menor que modelos avançados.
```

## Uso rápido

Clone o repositório:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
cd ognistie.skills
```

Depois, instale a pasta `skills/ognistie-skill` no Claude ou Codex e abra uma nova sessão.

## Guia para Claude Code

macOS ou Linux:

```bash
mkdir -p ~/.claude/skills
cp -R skills/ognistie-skill ~/.claude/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.claude\skills\ognistie-skill"
```

Use:

```text
/ognistie-skill Descreva aqui a tarefa que deseja analisar.
```

## Guia para OpenAI Codex

macOS ou Linux:

```bash
mkdir -p ~/.codex/skills
cp -R skills/ognistie-skill ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.codex\skills\ognistie-skill"
```

Use:

```text
$ognistie-skill Descreva aqui a tarefa que deseja analisar.
```

## Contribuindo

Faça um fork, crie uma branch com uma alteração objetiva e abra um pull request explicando o que foi modificado.

## Inspiração

Este repositório segue os padrões do [padrão Agent Skills](https://agentskills.io/) , [do repositório de habilidades da Anthropic](https://github.com/anthropics/skills) , [do repositório de habilidades da OpenAI](https://github.com/openai/skills).
