# ognistie.skills

## O que é

`ognistie-skill` é um roteador pré-tarefa para Claude e Codex. Ele analisa complexidade, risco, esforço e custo, recomenda o modelo OpenAI ou Anthropic mais econômico que atende ao nível de qualidade necessário e para sem executar a tarefa.

A skill não troca o modelo automaticamente. Ela ensina um fluxo simples:

1. Envie a tarefa para a skill.
2. Leia o modelo e o provedor recomendados.
3. Selecione esse modelo e envie a mesma tarefa para execução.

Resposta esperada:

```text
Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.
Motivo: Alteração visual moderada exige boa implementação com custo menor que modelos avançados.
```

Nenhum modelo garante perfeição. Tarefas críticas continuam exigindo testes, validações determinísticas e revisão humana.

## Uso rápido

Clone o repositório:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
cd ognistie.skills
```

Instale a pasta `skills/ognistie-skill` no Claude ou Codex e abra uma nova sessão.

## Guia para Claude Code

macOS ou Linux:

```bash
mkdir -p ~/.claude/skills/ognistie-skill
cp -R skills/ognistie-skill/. ~/.claude/skills/ognistie-skill/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills\ognistie-skill" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill\*" "$HOME\.claude\skills\ognistie-skill"
```

Use:

```text
/ognistie-skill Descreva aqui a tarefa que deseja analisar.
```

## Guia para OpenAI Codex

macOS ou Linux:

```bash
mkdir -p ~/.codex/skills/ognistie-skill
cp -R skills/ognistie-skill/. ~/.codex/skills/ognistie-skill/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills\ognistie-skill" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill\*" "$HOME\.codex\skills\ognistie-skill"
```

Use:

```text
$ognistie-skill Descreva aqui a tarefa que deseja analisar.
```

## Contribuindo

Faça um fork, crie uma branch objetiva e abra um pull request. Antes de enviar, execute:

```bash
python -B -m unittest discover -s tests -v
```

Mudanças no roteamento devem atualizar `evals/evals.json` e usar documentação oficial para modelos, preços e capacidades.

## Inspiração

Este repositório segue os padrões do [padrão Agent Skills](https://agentskills.io/) , [do repositório de habilidades da Anthropic](https://github.com/anthropics/skills) , [do repositório de habilidades da OpenAI](https://github.com/openai/skills).
