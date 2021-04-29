from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length



class BrukerSkjema(Form):
    nyBruker = StringField('Username: ', validators=[DataRequired()])
    fornavn = StringField('First name: ', validators=[DataRequired()])
    etternavn = StringField('Last name: ', validators=[DataRequired()])
    password = PasswordField('New Password: ', [
        validators.InputRequired(),
        validators.EqualTo('pwconfirm', message='Passwords must match')
     ])
    pwconfirm = PasswordField('Repeat Password: ')
    eMail = EmailField('E-mail Address: ', validators=[DataRequired(), Email(), Length(max=120)])
    brukernavn = HiddenField()
    submit = SubmitField('Submit form')

class loggInn(Form):
    brukernavn = StringField('Brukernavn: ', validators=[DataRequired()])
    passord = PasswordField('Passord: ', validators=[DataRequired()])
    submit = SubmitField('Submit form')



