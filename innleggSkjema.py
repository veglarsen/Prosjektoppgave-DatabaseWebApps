from wtforms import Form, StringField, HiddenField, SubmitField, validators, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length


class InnleggSkjema(Form):
    tittel = StringField('Title: ', validators=[DataRequired(), Length(max=20)])
    ingress = StringField('Preface text: ', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Body text: ', validators=[DataRequired(), Length(max=6000)])
    tag = SelectField(u'Tag: ', choices=selectTag)
    dato = DateField('Dato', validators=[DataRequired()])

    treff = StringField('First name: ', validators=[DataRequired()])
    innleggID = HiddenField()
    bloggID = HiddenField()
    submit = SubmitField('Submit form')

