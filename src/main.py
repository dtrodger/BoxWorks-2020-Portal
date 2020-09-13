"""
Application entry point for the Flask web app
"""
import os

from flask import Flask
from boxsdk.object.collaboration import CollaborationRole

from src.utils import get_box_client
from src.controllers import content_blueprint


flask_app = Flask(
    __name__, template_folder=os.path.join(os.path.dirname(__file__), "templates")
)
flask_app.config.update(SECRET_KEY="SECRET_KEY")
flask_app.register_blueprint(content_blueprint)


@flask_app.cli.command("set_up_box_client")
def set_up_box_client():
    """
    Sets up a Box Platform API client.
    """
    box_client = get_box_client()
    print(f"\nSet up Box Platform API client {box_client}\n")


@flask_app.cli.command("set_up_box_environment")
def set_up_box_environment():
    """
    Sets up a demo Box environment.
    """
    box_client = get_box_client()

    clients_folder = box_client.folder("0").create_subfolder("BoxWorks Clients")
    print(f"Created Clients folder with ID {clients_folder.response_object['id']}")

    client_folder = box_client.folder(clients_folder.response_object["id"]).create_subfolder("Smith & Co. Services")
    print(f"Created Smith & Co. Services Client folder with ID {client_folder.response_object['id']}")

    in_review_folder = box_client.folder(client_folder.response_object["id"]).create_subfolder("In Review")
    print(f"Created 'In Review' folder with ID {in_review_folder.response_object['id']}")

    approved_folder = box_client.folder(client_folder.response_object["id"]).create_subfolder("Approved")
    print(f"Created 'Approved' folder with ID {approved_folder.response_object['id']}")

    rejected_folder = box_client.folder(client_folder.response_object["id"]).create_subfolder("Rejected")
    print(f"Created 'Rejected'' folder with ID {rejected_folder.response_object['id']}")

    managed_user = box_client.create_user("Dave Rodgers", login="internaluser@acme.com")
    print(f"Created Box managed user with ID {managed_user.response_object['id']}")

    box_client.folder(client_folder.response_object["id"]).collaborate(managed_user, CollaborationRole.PREVIEWER)
    print(f"Created managed user previewer collaboration to the client folder")

    app_user = box_client.create_user("Sarah Jones")
    print(f"Created Smith & Co Employee Box app user with ID {app_user.response_object['id']}")

    box_client.folder(in_review_folder.response_object["id"]).collaborate(app_user, CollaborationRole.VIEWER_UPLOADER)
    print(f"Created app user viewer uploader collaboration to the client 'In Review' folder")

    box_client.folder(approved_folder.response_object["id"]).collaborate(app_user, CollaborationRole.VIEWER)
    print(f"Created app user viewer uploader collaboration to the 'Approved folder")

    box_client.folder(rejected_folder.response_object["id"]).collaborate(app_user, CollaborationRole.VIEWER)
    print(f"Created app user viewer uploader collaboration to the 'Rejected folder")
