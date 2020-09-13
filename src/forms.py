"""
Flask-WTF forms for server side form validation
"""
from flask_wtf import Form
from wtforms import (
    StringField,
    PasswordField
)
from wtforms.validators import (
    DataRequired,
    Email
)

from src.utils import validate_username_password


class LoginForm(Form):
    """
    User login form
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    def validate(self):
        """
        Validates that the submitted form data is associated to a user in the app's user store
        """
        valid = super().validate()
        if valid and not validate_username_password(
            self.email.data, self.password.data
        ):
            self.email.errors.append("Invalid email password combination.")
            valid = False

        return valid
