# Contributing

Thanks for improving `ognistie.skills`.

## Development workflow

1. Fork or clone the repository.
2. Create a focused branch from `main`.
3. Keep the canonical skill under `skills/ognistie-skill/`.
4. Update evaluation cases when behavior or model routing changes.
5. Run the complete test suite.
6. Review the diff for machine-specific paths, secrets, generated files, and unrelated changes.
7. Open a pull request describing the observable behavior change and validation evidence.

## Required checks

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

Optionally validate a captured response:

```bash
python skills/ognistie-skill/scripts/validate_routing_output.py response.txt
```

## Skill-writing rules

- Keep `SKILL.md` concise and imperative.
- Keep the YAML frontmatter limited to `name` and `description`.
- Put detailed examples and model mappings in `references/`.
- Never duplicate the canonical skill under platform folders.
- Use current official provider documentation for model changes.
- Do not embed credentials, private URLs, personal filesystem paths, or customer data.
- Preserve the two-line public response contract.

## Commit style

Prefer focused Conventional Commit messages, for example:

```text
feat: add a new routing capability
fix: enforce concise model recommendations
docs: clarify Claude installation
```
