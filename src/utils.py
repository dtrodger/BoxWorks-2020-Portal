"""
Utilities
"""

import logging.config
import os

import yaml
import boxsdk


log = logging.getLogger(__name__)


BOX_JWT_KEYS_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "..", "box_jwt_keys.yml"
)
IDP = {
    "drodgers@box.com": {
        "password": "Welcome2020",
        "box_app_user_id": "13761043560",
        "box_in_review_folder_id": "122234215069",
        "box_approved_folder_id": "122234461984",
        "box_rejected_folder_id": "122234675249",
    }
}
box_jwt_keys = None
box_client = None


def configure_logging():
    """
    Configure INFO level logging to stdout.
    """
    logging.basicConfig(level=logging.INFO)
    box_sdk_log = logging.getLogger("boxsdk")
    box_sdk_log.setLevel(logging.ERROR)


def get_box_jwt_keys():
    """
    Loads Box Platform JWT keys into a global variable.
    """
    global box_jwt_keys
    if not box_jwt_keys:
        with open(BOX_JWT_KEYS_FILE_PATH, "r") as fh:
            box_jwt_keys = yaml.load(fh, Loader=yaml.FullLoader)

    return box_jwt_keys


def get_box_auth():
    """
    Authenticates a Box SDK JWTAuth instance into Box Platform APIs.
    """
    box_jwt_keys = get_box_jwt_keys()
    box_auth = boxsdk.JWTAuth.from_settings_dictionary(box_jwt_keys)

    return box_auth


def get_box_client():
    """
    Sets up a Box Platform API client as a global variable.
    """
    global box_client
    if not box_client:
        box_auth = get_box_auth()
        box_client = boxsdk.Client(box_auth)

    return box_client


def validate_username_password(username, password):
    """
    Validates a username and password against the user store.
    """
    valid = False
    if (
        username in IDP.keys()
        and IDP[username]["password"] == password
    ):
        valid = True

    log.info(f"validated username {username} and password {password} to {valid}")

    return valid


def get_users_box_app_user_id(username):
    """
    Gets a user's Box app user ID.
    """
    return IDP[username]["box_app_user_id"]


def get_users_box_in_review_folder_id(username):
    """
    Gets a user's Box in review folder ID.
    """
    return IDP[username]["box_in_review_folder_id"]


def get_users_box_approved_folder_id(username):
    """
    Gets a user's Box approved folder ID.
    """
    return IDP[username]["box_approved_folder_id"]


def get_users_box_rejected_folder_id(username):
    """
    Gets a user's Box approved folder ID.
    """
    return IDP[username]["box_rejected_folder_id"]


def get_users_box_access_token(username):
    """
    Gets a user's Box Platform app user API access token
    """
    box_client = get_box_client()
    box_user_id = get_users_box_app_user_id(username)
    box_user = box_client.user(box_user_id)
    auth = boxsdk.JWTAuth.from_settings_dictionary(box_jwt_keys, user=box_user)
    auth.authenticate_user()
    box_as_user_client = boxsdk.Client(auth)

    return box_as_user_client._oauth.access_token
