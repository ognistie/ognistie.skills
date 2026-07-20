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

## Uso

Invoque a skill novamente para cada tarefa que deseja rotear.

No Codex:

```text
$ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

No Claude Code:

```text
/ognistie-skill:ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
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
