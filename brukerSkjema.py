from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class BrukerSkjema(Form):
    nyBruker = StringField('Username: ', validators=[DataRequired(), Length(max=20)])
    fornavn = StringField('First name: ', validators=[DataRequired(), Length(max=20)])
    etternavn = StringField('Last name: ', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('New Password: ', [
        validators.InputRequired(),
        validators.EqualTo('pwconfirm', message='Passwords must match')
     ])
    pwconfirm = PasswordField('Repeat Password: ')
    eMail = EmailField('E-mail Address: ', validators=[DataRequired(), Email(), Length(max=120)])
    brukernavn = HiddenField()
    submit = SubmitField('Submit form')

