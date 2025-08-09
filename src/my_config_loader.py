# src/config_loader.py

import os
from pathlib import Path
from dotenv import load_dotenv

def load_env(verbose: bool = False):
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if verbose:
        print(f"env_path=", env_path)
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        if verbose:
            print(f"[BOOTSTRAP] Loaded .env from {env_path}")
    else:
        if verbose:
            print("[BOOTSTRAP] ⚠️ .env file not found")

def get_config(key: str, default: str = None):
    return os.getenv(key, default)

