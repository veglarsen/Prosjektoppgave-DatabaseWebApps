from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators, SelectField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Email, Length, ValidationError
from database import myDB


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
    submit = SubmitField('Logg inn')


class loggInn(Form):
    brukernavn = StringField('Brukernavn: ', validators=[DataRequired()])
    passord = PasswordField('Passord: ', validators=[DataRequired()])
    submit = SubmitField('Submit form')


class NyBrukerSkjema(Form):
    brukernavn = StringField('Brukernavn: ', validators=[InputRequired(message='Brukernavn må spesifiseres'),
                                                         Length(min=3, max=20,
                                                                message='Brukernavn må være minst 3 tegn og maks 20 tegn')])
    fornavn = StringField('Fornavn: ',
                          validators=[InputRequired(message='Fornavn må spesifiseres'), Length(min=3, max=20)])
    etternavn = StringField('Etternavn: ',
                            validators=[InputRequired(message='Etternavn må spesifiseres'), Length(min=3, max=20)])
    password = PasswordField('Skriv inn passord: ', validators=[InputRequired(), validators.EqualTo('pwconfirm',
                                                                                                    message='Passordene må være identiske')])
    pwconfirm = PasswordField('Gjenta passordet')
    eMail = EmailField('E-post adresse: ', validators=[InputRequired(message='Epost adresse må spesifiseres'),
                                                       Email(message='En gyldig epost adresse må brukes'),
                                                       Length(min=3, max=120)])

    def validate_brukernavn(self, brukernavn):
        with myDB() as db:
            listUsernames = db.selectAllBrukernavn()
            if brukernavn.data in str(listUsernames):
                raise ValidationError(message="Brukernavn er allerede i bruk")

    submit = SubmitField('Submit form')
