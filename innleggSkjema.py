from wtforms import Form, StringField, HiddenField, SubmitField, SelectField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from database import myDB

with myDB() as db:
    selectTag = db.selectTag()
   # selectUser = db.selectBruker()


class NyttInnlegg(Form):
    tittel = StringField('Tittel: ', validators=[DataRequired(), Length(max=20)])
    ingress = StringField('Ingress: ', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Innlegg: ', validators=[DataRequired(), Length(max=6000)])  # cirka 2 sider
    tag = SelectField(u'Tag: ', choices=selectTag)
    newTag = StringField('Ny tag: ', validators=[DataRequired(), Length(max=10)])
    dato = DateField('Dato', validators=[DataRequired()])
    # innleggID = HiddenField() # tror ikke denne er nødvendig
    # trenger vedlegg!
    # bruker = StringField(selectUser)
    bloggID = HiddenField()
    submit = SubmitField('Legg til')
