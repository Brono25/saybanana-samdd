import base64
import json
import os


def get_credentials_obj_from_base64():
    """
    Firebase credentials are stored as a base64 data in the environment variable FIREBASE_CREDENTIALS_BASE64. Convert it to a dict.
    """
    base64_credentials = os.environ.get("FIREBASE_CREDENTIALS_BASE64")
    credentials_str = base64.b64decode(base64_credentials).decode("utf-8")
    credentials = json.loads(credentials_str)
    return credentials

BUCKET_PATH = os.environ.get("BUCKET_PATH")
WORKSPACE_VOLUME = os.environ.get("WORKSPACE_VOLUME")
CREDENTIALS = get_credentials_obj_from_base64()
