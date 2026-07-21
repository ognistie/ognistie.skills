# ognistie.skills

Skill de roteamento pré-tarefa: analisa uma tarefa e recomenda o modelo de menor custo que atende ao nível de qualidade e risco necessário.

A skill apenas recomenda o modelo. Ela não troca o modelo automaticamente e não executa a tarefa analisada.


https://github.com/user-attachments/assets/3b821a6a-00bd-46a2-a3b6-e8e7fa797e73

## Instalação

### <img src="https://raw.githubusercontent.com/shanraisshan/codex-cli-best-practice/b79f473a188632867354fc793894dfd368a18e48/!/codex-jumping.svg" width="42" alt="Mascote animado do Codex CLI"> OpenAI Codex

No Codex, instale a distribuição OpenAI pelo GitHub:

```text
$skill-installer Instale https://github.com/ognistie/ognistie.skills/tree/main/skills/codex/ognistie-skill
```

### <img src="https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/154e72475b5f85dd4b457ea36f38aaabac211718/!/claude-jumping.svg" width="42" alt="Mascote animado do Claude Code"> Claude Code

No Claude Code, adicione o marketplace e instale o plugin:

```text
/plugin marketplace add ognistie/ognistie.skills
/plugin install ognistie-skill@ognistie-skills
/reload-plugins
```

### <img src="https://raw.githubusercontent.com/shanraisshan/claude-code-best-practice/154e72475b5f85dd4b457ea36f38aaabac211718/!/claude-jumping.svg" width="42" alt="Mascote animado do Claude Code"> Claude Desktop

1. Baixe o pacote **[ognistie-skill-claude-desktop.zip](downloads/ognistie-skill-claude-desktop.zip)**.
2. No Claude Desktop, abra **Personalizar → Habilidades → Adicionar**.
3. Selecione **Fazer upload de uma habilidade** e envie o arquivo ZIP.
4. Ative a skill após o upload.

## Uso

Invoque a skill novamente para cada tarefa que deseja rotear.

 Codex:

```text
$ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

Claude Code:

```text
/ognistie-skill:ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

Claude Desktop:

```text
/ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```

Codex Desktop:
```text
$ognistie-skill Revise este fluxo OAuth procurando falhas de autorização.
```
## Resposta

A skill retorna somente o modelo, o provedor e uma justificativa curta:

```text
Modelo indicado: <modelo> — Provedor: <provedor>.
Motivo: <justificativa curta de qualidade, risco e custo>.
```

## Licença

[MIT](LICENSE)
