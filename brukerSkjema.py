from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class BrukerSkjema(Form):
    brukerNavn = StringField('Username', validators=[DataRequired()])
    forNavn = StringField('First name', validators=[DataRequired()])
    etterNavn = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.EqualTo('pwconfirm', message='Passwords must match')
     ])
    pwconfirm = PasswordField('Repeat Password')
    eMail = EmailField('E-mail Address', validators=[DataRequired(), Email(), Length(max=120)])
    ID = HiddenField()
    submit = SubmitField('Update user')

