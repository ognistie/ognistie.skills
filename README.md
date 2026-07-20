# ognistie.skills

Roteador pré-tarefa para escolher o modelo de menor custo que atende ao risco e à complexidade do trabalho. O repositório oferece distribuições independentes para Codex e Claude Code; nenhuma delas executa a tarefa ou troca o modelo automaticamente.

## Escolha seu ambiente

| Ambiente | Skill | Invocação | Modelos recomendados |
| --- | --- | --- | --- |
| OpenAI Codex | `skills/codex/ognistie-skill` | `$ognistie-skill <tarefa>` | OpenAI |
| Claude Code | `skills/claude/ognistie-skill` | `/ognistie-skill:ognistie-skill <tarefa>` | Anthropic |

Cada distribuição é autônoma e contém somente `SKILL.md`, licença, referências, validador e metadados exigidos pelo respectivo ambiente.

## Codex

Instale diretamente do GitHub:

```text
$skill-installer Instale https://github.com/ognistie/ognistie.skills/tree/main/skills/codex/ognistie-skill
```

Se a skill não aparecer após a instalação, reinicie o Codex. Depois use:

```text
$ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

O nome curto no `$skill-installer` dependerá da aceitação da distribuição Codex em `openai/skills/skills/.curated/ognistie-skill`.

## Claude Code

### Instalação recomendada

Pré-requisito: use uma versão recente do Claude Code que reconheça o comando `/plugin`. Se o comando não aparecer, atualize o Claude Code e reinicie a sessão.

Dentro do Claude Code, execute cada comando separadamente:

```text
/plugin marketplace add ognistie/ognistie.skills
/plugin install ognistie-skill@ognistie-skills
/reload-plugins
```

Confirme que o plugin aparece entre os instalados:

```text
/plugin list
```

Agora envie uma tarefa concreta:

```text
/ognistie-skill:ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

Por ser distribuída como plugin, a skill recebe o namespace `ognistie-skill`. Ela apenas recomenda um modelo Anthropic; não troca o modelo nem executa a tarefa.

#### Atualizar

```text
/plugin marketplace update ognistie-skills
/plugin update ognistie-skill@ognistie-skills
/reload-plugins
```

#### Desinstalar

```text
/plugin uninstall ognistie-skill@ognistie-skills
/plugin marketplace remove ognistie-skills
```

#### Solução de problemas

- Se `/plugin` não existir, atualize o Claude Code.
- Se o marketplace não for encontrado, confirme o acesso a `github.com/ognistie/ognistie.skills` e repita o primeiro comando.
- Se a skill não aparecer depois da instalação, execute `/reload-plugins` ou reinicie o Claude Code.
- Use `/ognistie-skill:ognistie-skill`; `/ognistie.skill` não é um comando válido.

### Instalação manual

Para manter o comando curto `/ognistie-skill`, clone o repositório e copie a distribuição Claude para sua pasta pessoal.

macOS ou Linux:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
mkdir -p ~/.claude/skills/ognistie-skill
cp -R ognistie.skills/skills/claude/ognistie-skill/. ~/.claude/skills/ognistie-skill/
```

Windows PowerShell:

```powershell
git clone https://github.com/ognistie/ognistie.skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills\ognistie-skill" | Out-Null
Copy-Item -Recurse -Force ".\ognistie.skills\skills\claude\ognistie-skill\*" "$HOME\.claude\skills\ognistie-skill"
```

Depois use:

```text
/ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

Use o hífen exatamente como mostrado. `/ognistie.skill` não é um comando válido. Na instalação manual, o Claude Code deriva `/ognistie-skill` do nome da pasta.

Se a pasta `~/.claude/skills` não existia quando a sessão começou, reinicie o Claude Code para habilitar a descoberta.

## Saída

As duas distribuições retornam somente:

```text
Modelo indicado: <modelo> — Provedor: <provedor>.
Motivo: <justificativa curta de qualidade, risco e custo>.
```

Tarefas críticas continuam exigindo testes, verificações determinísticas e aprovação humana.

## Desenvolvimento

```text
evals/      Casos compartilhados de economy, balanced, advanced e segurança
scripts/    Ferramentas de avaliação do repositório
skills/     Distribuições autônomas para Codex e Claude Code
tests/      Validação estrutural e comportamental das duas distribuições
```

Antes de contribuir, execute:

```bash
python -B -m unittest discover -s tests -v
python -m ruff check scripts tests skills
```

Para avaliar respostas capturadas:

```bash
python scripts/evaluate_routing_outputs.py skills/codex/ognistie-skill outputs.json
python scripts/evaluate_routing_outputs.py skills/claude/ognistie-skill outputs.json
```

Mudanças de política devem atualizar `evals/evals.json`. Mudanças de modelos, preços ou disponibilidade devem usar as fontes oficiais registradas em cada catálogo.

## Licença

[MIT](LICENSE)
