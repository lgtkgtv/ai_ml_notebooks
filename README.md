# README.md

```bash
uv run --with jupyterlab jupyter lab --no-browser
```

I’ve integrated it cleanly under the setup section and explained when and why to use the `--no-browser` flag.

---

### ✅ Final Updated `README.md`

````markdown
# 📘 my-ai-project

A reproducible, secure-by-default Python AI/ML project managed using [uv](https://docs.astral.sh/uv/), structured for Jupyter notebooks and DevOps integration.

---

## 🧰 Project Features

- ✅ Isolated Python environment using `uv`
- ✅ Reproducible dependency locking with `uv.lock`
- ✅ JupyterLab integration with project-specific kernel
- ✅ Support for AI/ML libraries (e.g. numpy, pandas, scikit-learn)
- ✅ Secure DevOps practices with `uv run`, linting, CI/CD-ready
- ✅ Recommended structure for clean project organization

---

## 🛠️ Setup Instructions

### 1. Install `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
````

### 2. Initialize the project

```bash
mkdir ai_ml_notebooks
cd ai_ml_notebooks
uv init
```

### 3. Add dependencies

```bash
uv add --dev jupyterlab ipykernel numpy pandas scikit-learn matplotlib
uv add --dev torch torchvision torchaudio
```

### 4. Register your Jupyter kernel (fixed & clean)

```bash
VIRTUAL_ENV=$(pwd)/.venv uv run ipython kernel install \
  --user \
  --name=ai_ml_notebooks \
  --display-name "ai_ml_notebooks"
```

📌 After running, verify it:

```bash
cat ~/.local/share/jupyter/kernels/ai_ml_notebooks/kernel.json
```

---

## 🚀 Launch JupyterLab

To run JupyterLab with your `uv`-managed environment:

### ▶️ Normal (opens in browser):

```bash
uv run --with jupyterlab jupyter lab
```

### ⚙️ Headless or remote access (no browser auto-launch):

```bash
uv run --with jupyterlab jupyter lab --no-browser
```

Use this in environments like:

* Remote SSH sessions
* Tmux/screen-based workflows
* Docker containers or VS Code DevContainers

Then access via:

```
http://localhost:8888/?token=...
```

---

## 📂 Recommended Project Layout

```text
ai_ml_notebooks/
├── .venv/                  # uv-managed virtualenv
├── .python-version         # Python version pin (optional)
├── README.md               # Project info and usage guide
├── pyproject.toml          # Declared dependencies
├── uv.lock                 # Locked dependencies
├── notebooks/              # Jupyter notebooks live here
│   └── <analysis>.ipynb
├── src/                    # Modular code
│   └── <my_module>.py
└── main.py                 # Optional script entry point
```

---

## 🚀 Common uv Commands

| Task                    | Command                                             |
| ----------------------- | --------------------------------------------------- |
| Add dependency          | `uv add <pkg>`                                      |
| Add dev-only dependency | `uv add --dev <pkg>`                                |
| Remove dependency       | `uv remove <pkg>`                                   |
| Lock dependencies       | `uv lock`                                           |
| Sync environment        | `uv sync`                                           |
| Run script or tool      | `uv run <cmd>`                                      |
| Run JupyterLab          | `uv run --with jupyterlab jupyter lab`              |
| Run headless            | `uv run --with jupyterlab jupyter lab --no-browser` |
| Format/lint             | `uvx ruff` / `uvx black`                            |

---

## 🧠 Detailed Explanation of Kernel Setup Command

```bash
VIRTUAL_ENV=$(pwd)/.venv uv run ipython kernel install \
  --user \
  --name=my-ai-project \
  --display-name "my-ai-project"
```

| Part                        | Purpose                                   |
| --------------------------- | ----------------------------------------- |
| `VIRTUAL_ENV=$(pwd)/.venv`  | Temporarily sets virtual environment path |
| `uv run`                    | Activates the uv-managed `.venv`          |
| `ipython kernel install`    | Registers a Jupyter kernel                |
| `--user`                    | Local install, no sudo                    |
| `--name` / `--display-name` | Sets kernel identifier and UI label       |

---

## 🔐 Secure Coding & DevOps Tips

* Always commit `pyproject.toml` and `uv.lock` for reproducibility
* Use `uv run` in CI/CD to ensure deterministic builds and tests
* Use `uvx` to isolate dev tools from runtime dependencies
* Manage secrets using `.env` (never hardcode in notebooks or scripts)

---

## 📌 Future Enhancements

* [ ] Add CI/CD pipeline (GitHub Actions)
* [ ] Integrate `pytest` and fuzz harness
* [ ] Build tutorial notebooks for SHAP, backdoor detection
* [ ] Auto-load `.env` for project-level config
* [ ] Dockerize notebook runtime for portability

---

## 🙋 About

Built with `uv` and Jupyter for hands-on AI/ML development, secure coding, and DevSecOps automation.

---

## License

MIT (or your preferred license)

```

------------------------------------------------------------------------------------------------------


# ✅ Stage 1: Modular `.env` Loader for Cloud + API Integration

---

## 🧱 Project Layout (Confirmed)

```text
ai_ml_notebooks/
├── .env                         # Project secrets + config
├── notebooks/
│   └── 01-pytorch-secure-intro.ipynb
├── src/
│   └── config_loader.py         # loads env vars for notebooks and modules
```

---

## 📄 Step 1: Create a `.env` File

```ini
# === API Keys ===
OPENAI_API_KEY=
# === Project Config ===
PROJECT_NAME=ai_ml_notebooks
PROJECT_ROOT_DIR=/home/s/lgtk/ai_ml_notebooks
ENV=dev
```

> ⚠️ **Never commit this file.** Add `.env` to `.gitignore`.

---

## 🐍 Step 2: Add a `config_loader.py` in `src/`

```python
# src/config_loader.py

import os
from pathlib import Path
from dotenv import load_dotenv

def load_env(verbose: bool = False):
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        if verbose:
            print(f"[INFO] Loaded .env from {env_path}")
    else:
        if verbose:
            print("[WARN] No .env file found")

def get_config(key: str, default: str = None):
    return os.getenv(key, default)
```

---

## 📥 Step 3: Install `python-dotenv`

```bash
uv add --dev python-dotenv
```

---

## ✅ Step 4: Use it inside notebooks

```python
# Inside notebooks/01-pytorch-secure-intro.ipynb

from src.config_loader import load_env, get_config

load_env(verbose=True)

openai_key = get_config("OPENAI_API_KEY")
aws_key = get_config("AWS_ACCESS_KEY_ID")
```

Use `get_config(...)` for secrets and project settings across your modules and notebooks securely and consistently.

---

# ✅ Stage 2: PyTorch Notebook with Security-First Foundations

---

## 🧪 File: `notebooks/01-pytorch-secure-intro.ipynb`

This notebook includes:

* Project config loading
* PyTorch installation check
* Model and data sanity check
* Explicit error handling
* Reproducibility seeds

```

---

## ✅ Notebook Highlights

It includes:

* ✅ `.env` loading via `src/config_loader.py`
* ✅ PyTorch environment checks
* ✅ Reproducibility best practices (manual seeds)
* ✅ Minimal `nn.Module` setup for experimentation
* ✅ Sanity-checked dummy inference

---

## 🔁 Next Steps

1. **Start your JupyterLab**:

   ```bash
   uv run --with jupyterlab jupyter lab --no-browser
   ```

2. **Open** `notebooks/01-pytorch-secure-intro.ipynb`
   Select the `ai_ml_notebooks` kernel.

3. ✅ Test cell-by-cell and confirm `torch`, `.env`, and your model behave as expected.

---

Would you like me to now:

* Add `scripts/setup_env.sh` to bootstrap `.env` and `.venv`?
* Scaffold a `src/training.py` module with secure data pipeline/loading?
* Help you containerize this setup with Docker and `.env` secrets mounting?

---

### Checkin `uv.lock` ?

Yes — commit uv.lock if this is an application, not a library
  The lock file pins exact versions of dependencies (including transitive ones).
  This ensures reproducible installs across machines, CI, and deployments.
  Your teammates and CI/CD will get exactly the same versions you developed against.

```
# team member / CI
uv sync
```

No — don’t commit if this is a reusable library published to PyPI
Libraries should specify version ranges in pyproject.toml, letting downstream apps resolve.

### Git best practice if you commit it:

Add it to `.gitattributes` for diff friendliness:

```
uv.lock text eol=lf
```

Treat updates to `uv.lock` as code changes — review them in PRs to catch dependency changes or security issues.

### Security angle for your workflows

Commit uv.lock for applications → makes supply chain audits and SBOM generation easier.
You can run `trivy fs` or `pip-audit` on the lock file to detect vulnerable dependencies before deployment.

#### CI enforcement: fail PRs if lockfile is stale or missing

create  `.github/workflows/lockfile.yml`

```
name: Lockfile guard

on:
  pull_request:
    paths:
      - "pyproject.toml"
      - "uv.lock"
      - ".github/workflows/lockfile.yml"

jobs:
  check-lock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          enable-cache: true

      - name: Ensure lockfile exists & is up to date (no changes allowed)
        run: |
          # Fail if uv.lock would change or is missing
          uv lock --check
        # `uv lock --check` == assert lock is current; error if it would change. :contentReference[oaicite:0]{index=0}

      - name: Enforce “pyproject changed ⇒ uv.lock changed”
        if: ${{ github.event_name == 'pull_request' }}
        run: |
          set -eux
          BASE_SHA="${{ github.event.pull_request.base.sha }}"
          HEAD_SHA="${{ github.sha }}"
          CHANGED_FILES="$(git diff --name-only "$BASE_SHA" "$HEAD_SHA")"

          if echo "$CHANGED_FILES" | grep -q '^pyproject\.toml$'; then
            if ! echo "$CHANGED_FILES" | grep -q '^uv\.lock$'; then
              echo "::error ::pyproject.toml changed but uv.lock did not. Run 'uv lock' and commit the result."
              exit 1
            fi
          fi

      - name: Frozen sync sanity (optional)
        run: |
          # Install strictly from lock without updating it
          uv sync --locked
        # `uv sync --locked` avoids re-locking and asserts lock consistency. :contentReference[oaicite:1]{index=1}
```
* `uv lock --check` (alias --locked) **fails** if `uv.lock` is missing or would change → perfect for CI.
* `uv sync --locked` installs from the lock **without** updating it. Good sanity check for reproducibility.


#### Branch protection / ruleset (GitHub)

In Settings → Code and automation → Branches → Branch protection rules for main:

1. **Require a pull request before merging** (block direct pushes).
2. **Require status checks to pass** and select the workflow check “Lockfile guard”.
3. Optional but recommended:
      Require signed commits (SSH signing is painless).
      Require linear history.
      Include administrators so everyone follows the rules.

**Local guardrails (pre-commit)**

* **Catch secrets & formatting before they ever hit CI:**
```
pipx install pre-commit detect-secrets
pre-commit sample-config > .pre-commit-config.yaml
detect-secrets scan > .secrets.baseline
```

* **Append to `.pre-commit-config.yaml`:**
```
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-merge-conflict
      - id: check-added-large-files
        args: ['--maxkb=5000']
      - id: end-of-file-fixer
      - id: trailing-whitespace
```

Enable:
```
pre-commit install
```
