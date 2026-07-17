# Anthropic Claude Code installation

The canonical skill is [`../../skills/ognistie-skill`](../../skills/ognistie-skill). Claude uses the same `SKILL.md` and supporting resources as OpenAI Codex.

## Personal installation

### macOS or Linux

```bash
mkdir -p ~/.claude/skills
cp -R skills/ognistie-skill ~/.claude/skills/
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.claude\skills\ognistie-skill"
```

Start a new Claude Code session, then invoke:

```text
/ognistie-skill <describe one task>
```

Claude may also invoke the skill automatically when the task matches its description.

## Project installation

For a repository-scoped skill, copy the canonical folder to:

```text
<project>/.claude/skills/ognistie-skill
```

## Update

Pull the latest repository version and repeat the copy command. Review local modifications before replacing an existing customized installation.
