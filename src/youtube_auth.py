import os
import sys
import logging
from typing import Optional
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
DEFAULT_CLIENT_SECRET_FILE = os.getenv("YTCLI_CLIENT_SECRET", "client_secret.json")

def normalize_account_id(account: str) -> str:
    return account.replace("@", "_at_").replace(".", "_dot_")

def get_authenticated_youtube(account: str,
                               scopes: Optional[list] = None,
                               client_secret_file: Optional[str] = None,
                               headless: bool = False):
    scopes = scopes or SCOPES
    client_secret_file = client_secret_file or DEFAULT_CLIENT_SECRET_FILE
    print(f"client_secret_file", client_secret_file)

    if not os.path.exists(client_secret_file):
        raise FileNotFoundError(f"Missing client_secret.json at: {client_secret_file}")

    os.makedirs("tokens", exist_ok=True)
    norm = normalize_account_id(account)
    token_file = os.path.join("tokens", f"{norm}.json")

    creds = None

    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, scopes)
        except Exception as e:
            logger.warning(f"Failed to load credentials from {token_file}: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info(f"Refreshed token for account: {account}")
            except Exception as e:
                logger.warning(f"Token refresh failed: {e}")
                creds = None

        if not creds or not creds.valid:
            logger.info("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            creds = flow.run_console() if headless else flow.run_local_server(port=0)

        with open(token_file, "w") as token:
            token.write(creds.to_json())
        os.chmod(token_file, 0o600)

    return build("youtube", "v3", credentials=creds)
