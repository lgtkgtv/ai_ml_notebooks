# GUARDRAILS.md

# Guardrails

This repo uses:
- `.github/workflows/lockfile.yml` to ensure `uv.lock` stays in sync with `pyproject.toml`.
- `pre-commit` with `detect-secrets` to block committing secrets.

## Local setup

```bash
pipx install pre-commit detect-secrets
pre-commit install
detect-secrets scan > .secrets.baseline
git add .secrets.baseline .pre-commit-config.yaml
git commit -m "chore(pre-commit): add secrets baseline"
```

---


Once you’ve created these:

```bash
git checkout -b chore/lockfile-guard
git add .gitignore .github/workflows/lockfile.yml .pre-commit-config.yaml GUARDRAILS.md
git commit -m "chore(guardrails): lockfile CI + pre-commit secrets scan"
git push -u origin chore/lockfile-guard
```

Then open a PR and set up branch protection to require the **Lockfile guard** workflow to pass.


