from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired(), validators.input_required()])
    password = PasswordField('Password', [validators.DataRequired(), validators.input_required()])