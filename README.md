# ognistie.skills

Skill de roteamento pré-tarefa: analisa uma tarefa e recomenda o modelo de menor custo que atende ao nível de qualidade e risco necessário.

A skill apenas recomenda o modelo. Ela não troca o modelo automaticamente e não executa a tarefa analisada.

## Instalação

### OpenAI Codex

No Codex, instale a distribuição OpenAI pelo GitHub:

```text
$skill-installer Instale https://github.com/ognistie/ognistie.skills/tree/main/skills/codex/ognistie-skill
```

### Claude Code

No Claude Code, adicione o marketplace e instale o plugin:

```text
/plugin marketplace add ognistie/ognistie.skills
/plugin install ognistie-skill@ognistie-skills
/reload-plugins
```

Para manter o comando curto `/ognistie-skill`, copie manualmente a distribuição Claude:

```bash
git clone https://github.com/ognistie/ognistie.skills.git
mkdir -p ~/.claude/skills/ognistie-skill
cp -R ognistie.skills/skills/claude/ognistie-skill/. ~/.claude/skills/ognistie-skill/
```

No Windows PowerShell:

```powershell
git clone https://github.com/ognistie/ognistie.skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills\ognistie-skill" | Out-Null
Copy-Item -Recurse -Force ".\ognistie.skills\skills\claude\ognistie-skill\*" "$HOME\.claude\skills\ognistie-skill"
```

## Uso

Invoque a skill novamente para cada tarefa que deseja rotear.

No Codex:

```text
$ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

No Claude Code instalado como plugin:

```text
/ognistie-skill:ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

No Claude Code instalado manualmente:

```text
/ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

`/ognistie.skill` não é um comando válido. Use hífen e invoque a skill em cada nova tarefa.

## Resposta

A skill retorna somente o modelo, o provedor e uma justificativa curta:

```text
Modelo indicado: <modelo> — Provedor: <provedor>.
Motivo: <justificativa curta de qualidade, risco e custo>.
```

## Licença

[MIT](LICENSE)
