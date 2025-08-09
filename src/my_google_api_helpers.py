# my_google_api_helpers.py
"""
------------------------------------------------------------------------------
| Feature                         | Where                                         |
| ------------------------------- | --------------------------------------------- |
| Load YAML config                | `load_scope_profiles`, `load_user_api_config` |
| Normalize user ID               | `normalize_account_id`                        |
| Cache tokens per user+API+scope | `tokens/{user}__{api}__{scope}.json`          |
| Reuse token if valid            | `Credentials.from_authorized_user_file()`     |
| Refresh token if expired        | `creds.refresh()`                             |
| Start new OAuth flow if needed  | `flow.run_local_server()`                     |
| Save refreshed/issued token     | `token.write(creds.to_json())`                |
------------------------------------------------------------------------------
"""

import os
import yaml
import logging
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("google_api_helper")

# Default config paths
CONFIG_SCOPE_PATH = "config/google_api_scopes.yaml"
CONFIG_USERS_PATH = "config/google_users.yaml"
DEFAULT_TOKEN_DIR = "tokens"

# 1. Normalize Email for Safe Filename
#
#   transforms: lgtkgtv@gmail.com → lgtkgtv_at_gmail_dot_com
#   Used for token file naming `tokens/lgtkgtv_at_gmail_dot_com__gmail__send.json`
#
def normalize_account_id(account_email: str) -> str:
    return account_email.replace("@", "_at_").replace(".", "_dot_")

# 2. Load API Scopes configurations for Google's OAUTH2 based APIs
#
# youtube:
#  read:
#    - https://www.googleapis.com/auth/youtube.readonly
#  write:
#    - https://www.googleapis.com/auth/youtube.force-ssl
#
def load_scope_profiles(yaml_path: str = CONFIG_SCOPE_PATH) -> dict:
    with open(yaml_path) as f:
        return yaml.safe_load(f)

# 2. Load API scopes configured per Google users account -- These will be requested by this app
# - user: lgtkgtv@gmail.com
#  apis:
#    youtube: write
#    
def load_user_api_config(yaml_path: str = CONFIG_USERS_PATH) -> list:
    with open(yaml_path) as f:
        return yaml.safe_load(f)


# 3. Select Scopes for a Given API + Profile
#
#   get_scopes_for("gmail", "send", scope_yaml)
#   → ["https://www.googleapis.com/auth/gmail.send"]
#
def get_scopes_for(api: str, profile: str, scope_config: dict) -> list:
    try:
        return scope_config[api][profile]
    except KeyError:
        raise ValueError(f"Scope profile '{profile}' not defined for API '{api}'")


# Main function to get authenticated client
def get_google_api_client(api_name: str,
                          scope_profile: str,
                          account_email: str,
                          client_secret_file: str = None,
                          scopes_config_path: str = CONFIG_SCOPE_PATH) -> object:
    # Load scopes
    scopes_config = load_scope_profiles(scopes_config_path)
    scopes = get_scopes_for(api_name, scope_profile, scopes_config)

    # Prepare token path
    norm = normalize_account_id(account_email)
    token_dir = Path(DEFAULT_TOKEN_DIR)
    token_dir.mkdir(exist_ok=True)
    token_file = token_dir / f"{norm}__{api_name}__{scope_profile}.json"

    creds = None

    # Load token if exists
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(token_file, scopes)

    # Refresh or authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            logger.info(f"🔄 Refreshed token for {account_email} - {api_name}")
        else:
            # Use default or env override
            client_secret_file = client_secret_file or os.getenv("GOOGLE_CLIENT_SECRET", "secret/client_secret.json")
            if not Path(client_secret_file).exists():
                raise FileNotFoundError(f"❌ Missing client_secret.json at: {client_secret_file}")
            # Launch OAuth Consent Flow
            logger.info(f"🌐 Starting OAuth flow for {account_email} - {api_name} ({scope_profile})")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            creds = flow.run_local_server(port=0)  # Receives access_token + refresh_token

        # Save token for reuse
        with open(token_file, "w") as token:
            token.write(creds.to_json())
            logger.info(f"✅ Token saved: {token_file.name}")

    return build(api_name, "v3", credentials=creds)


## Token Isolation Per (User, API, Scope)
#
# This structure ensures:
#    Each user has their own tokens
#    Changing one user’s scope or API doesn’t affect others
#    Scope mismatches are detected and handled

## Example Token File
#
# tokens/lgtkgtv_at_gmail_dot_com__gmail__send.json
#
# {
#  "token": "ya29....",
#  "refresh_token": "1//0g....",
#  "scopes": ["https://www.googleapis.com/auth/gmail.send"],
#  ...
# }

