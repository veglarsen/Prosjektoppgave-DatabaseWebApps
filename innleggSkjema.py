from wtforms import Form, StringField, HiddenField, SubmitField, validators, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length


class InnleggSkjema(Form):
    tittel = StringField('Title: ', validators=[DataRequired()])
    ingress = StringField('Preface text: ', validators=[DataRequired()])
    innlegg = TextAreaField(' ', validators=[DataRequired(), Length(max=250)])
    tag = SelectField(u'kategorier', choices=selectTag)
    dato = DateField('Dato', validators=[DataRequired()])

    treff = StringField('First name: ', validators=[DataRequired()])
    innleggID = HiddenField()
    bloggID = HiddenField()
    submit = SubmitField('Submit form')

