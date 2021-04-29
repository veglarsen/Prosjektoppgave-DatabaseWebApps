from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash



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

class loggInn(Form):

    brukernavn = StringField('Brukernavn: ', validators=[DataRequired()])
    passord = PasswordField('Passord: ', validators=[DataRequired()])
    submit = SubmitField('Submit form')

class NyBrukerSkjema(Form):
    brukernavn = StringField('Username: ', validators=[DataRequired(), Length(max=20)])
    fornavn = StringField('First name: ', validators=[DataRequired(), Length(max=20)])
    etternavn = StringField('Last name: ', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('New Password: ')
    # hashedPassword = generate_password_hash(password)
    # pwconfirm = PasswordField('Repeat Password: ', [
    #     validators.InputRequired(),
    #     validators.EqualTo('password', message='Passwords must match')
    #  ])
    pwconfirm = PasswordField('Repeat Password: ', [validators.InputRequired(), validators.EqualTo('password', message='Passwords must match')])
    eMail = EmailField('E-mail Address: ', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Submit form')
