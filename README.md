# ognistie.skills

## O que é

`ognistie-skill` é um roteador pré-tarefa para Claude e Codex. Ele analisa complexidade, risco, esforço e custo, recomenda o modelo OpenAI ou Anthropic mais econômico que atende ao nível de qualidade necessário e para sem executar a tarefa.

A skill não troca o modelo automaticamente. Ela ensina um fluxo simples:

1. Invoque a skill e escreva a tarefa na mesma mensagem.
2. Leia o modelo e o provedor recomendados.
3. Selecione esse modelo e envie a mesma tarefa para execução.

Resposta esperada:

```text
Modelo indicado: Claude Sonnet 5 — Provedor: Anthropic.
Motivo: Alteração visual moderada exige boa implementação com custo menor que modelos avançados.
```

Nenhum modelo garante perfeição. Tarefas críticas continuam exigindo testes, validações determinísticas e revisão humana.

> A ativação vale para a mensagem atual. Não envie `$ognistie-skill` sozinho e a tarefa depois; use sempre `$ognistie-skill <sua tarefa>` em uma única mensagem.

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
/ognistie-skill Descreva aqui a tarefa que deseja analisar, na mesma mensagem.
```

## Guia para OpenAI Codex

Instalação direta pelo catálogo de skills do Codex:

```text
$skill-installer Instale https://github.com/ognistie/ognistie.skills/tree/main/skills/ognistie-skill
```

Se a skill não aparecer imediatamente após a instalação, reinicie o Codex. Até que ela seja aceita no catálogo oficial `openai/skills`, a instalação deve informar a URL completa; o nome curto `$skill-installer ognistie-skill` fica disponível somente após inclusão em `skills/.curated/ognistie-skill`.

Instalação manual:

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
$ognistie-skill Descreva aqui a tarefa que deseja analisar, na mesma mensagem.
```

## Contribuindo

Faça um fork, crie uma branch objetiva e abra um pull request. Antes de enviar, execute:

```bash
python -B -m unittest discover -s tests -v
```

Mudanças no roteamento devem atualizar `evals/evals.json` e usar documentação oficial para modelos, preços e capacidades.

Para propor a skill ao catálogo oficial, faça um fork de `openai/skills`, adicione a pasta em `skills/.curated/ognistie-skill` e abra um pull request para avaliação dos mantenedores.

## Inspiração

Este repositório segue os padrões do [padrão Agent Skills](https://agentskills.io/) , [do repositório de habilidades da Anthropic](https://github.com/anthropics/skills) , [do repositório de habilidades da OpenAI](https://github.com/openai/skills).
