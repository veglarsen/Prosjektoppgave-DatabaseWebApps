from wtforms import Form, StringField, HiddenField, SubmitField, PasswordField, validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class InnleggSkjema(Form):
    tittel = StringField('First name: ', validators=[DataRequired()])
    ingress = StringField('First name: ', validators=[DataRequired()])
    treff = StringField('First name: ', validators=[DataRequired()])
    tag = StringField('First name: ', validators=[DataRequired()])
    dato = StringField('First name: ', validators=[DataRequired()])

    innlegg = StringField('Last name: ', validators=[DataRequired()])
    innleggID = HiddenField()
    bloggID = HiddenField()
    submit = SubmitField('Submit form')

