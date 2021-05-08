from wtforms import Form, StringField, HiddenField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length


class NyttInnlegg(Form):
    tittel = StringField('Tittel: ', validators=[DataRequired(), Length(max=20)])
    ingress = StringField('Ingress: ', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Innlegg: ', validators=[DataRequired(), Length(max=6000)])  # cirka 2 sider
    tag = SelectMultipleField(u'Tag: ', choices=[])
    newTag = StringField('Ny tag: ', validators=[Length(max=10)])  # kan ikke være DataRequired(),
    # trenger vedlegg!
    bloggID = HiddenField()
    submit = SubmitField('Legg til')

class SearchForm(Form):
    searchField = StringField('Søk i alle innlegg', validators=[Length(max=20)])  # validator!
    tag = SelectMultipleField(u'Tag: ', choices=[])
    submit = SubmitField('SØK')

class RedigerInnleggForm(Form):
    tittel = StringField('Tittel', validators=[DataRequired(), Length(max=20)])               #REDIGER LENGDEN
    ingress = StringField('Ingress', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Innlegg Tekst', validators=[DataRequired(), Length(max=250)])
    id = HiddenField()
    tag = SelectMultipleField(u'Tag: ', choices=[])
    newTag = StringField('Ny tag: ', validators=[Length(max=10)])
    submit = SubmitField('Update')

class NyBlogg(Form):
    blogg_navn = StringField('Blogg Navn: ', validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('Legg til')