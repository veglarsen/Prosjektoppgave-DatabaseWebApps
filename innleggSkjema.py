from wtforms import Form, StringField, HiddenField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from database import myDB

with myDB() as db:
    selectTag = db.selectTag()
   # selectUser = db.selectBruker()


class InnleggSkjema(Form):
    tittel = StringField('Title: ', validators=[DataRequired(), Length(max=20)])
    ingress = StringField('Preface text: ', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Body text: ', validators=[DataRequired(), Length(max=6000)])  # cirka 2 sider
    tag = SelectField(u'Tag: ', choices=selectTag)
    newTag = StringField('New tag: ', validators=[DataRequired(), Length(max=10)])
    dato = DateField('Dato', validators=[DataRequired()])
    # innleggID = HiddenField() # tror ikke denne er nødvendig
    # bruker = StringField(selectUser)
    bloggID = HiddenField()
    submit = SubmitField('Submit form')
