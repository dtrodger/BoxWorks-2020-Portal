"""
Flask controllers to process HTTP requests
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort
)

from src.forms import LoginForm
from src.utils import (
    get_users_box_in_review_folder_id,
    get_users_box_approved_folder_id,
    get_users_box_access_token,
    get_users_box_rejected_folder_id
)


content_blueprint = Blueprint("content", __name__, url_prefix="/content/")


@content_blueprint.route("login/", methods=["GET", "POST"])
def login():
    """
    Login request handler
    """
    if request.method == "GET":
        login_form = LoginForm()
        return render_template("login.html", login_form=login_form)

    elif request.method == "POST":
        login_form = LoginForm(request.form)
        if login_form.validate_on_submit():
            session.update(authenticated=True, username=login_form.email.data)
            return redirect(url_for("content.view"))
        else:
            return render_template("login.html", login_form=login_form)


@content_blueprint.route("logout/", methods=["GET"])
def logout():
    """
    Logout request handler
    """
    session.update(authenticated=False, username=None)

    return redirect(url_for("content.login"))


@content_blueprint.route("", methods=["GET"])
def view():
    """
    View Box content request handler
    """
    if not session.get("authenticated"):
        abort(404)

    username = session["username"]

    return render_template(
        "content.html",
        box_access_token=get_users_box_access_token(username),
        box_in_review_folder_id=get_users_box_in_review_folder_id(username),
        box_approved_folder_id=get_users_box_approved_folder_id(username),
        box_rejected_folder_id=get_users_box_rejected_folder_id(username)
    )
