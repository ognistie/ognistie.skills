# OpenAI Codex installation

The canonical skill is [`../../skills/ognistie-skill`](../../skills/ognistie-skill). Do not maintain a second platform-specific copy.

## Personal installation

### macOS or Linux

```bash
mkdir -p ~/.codex/skills
cp -R skills/ognistie-skill ~/.codex/skills/
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\skills\ognistie-skill" "$HOME\.codex\skills\ognistie-skill"
```

Start a new Codex task, then invoke:

```text
$ognistie-skill <describe one task>
```

Codex reads `agents/openai.yaml` for the display name and default prompt. The skill itself remains portable.

## Update

Pull the latest repository version and repeat the copy command. Review local modifications before replacing an existing customized installation.
