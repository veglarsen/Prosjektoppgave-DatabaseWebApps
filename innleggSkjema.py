from wtforms import Form, StringField, HiddenField, SubmitField, SelectField, TextAreaField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

from blogg import Tag
from database import myDB

with myDB() as db:
    selectTag = db.selectTag()
    print(selectTag)
   # selectUser = db.selectBruker()


class NyttInnlegg(Form):
    tittel = StringField('Tittel: ', validators=[DataRequired(), Length(max=20)])
    ingress = StringField('Ingress: ', validators=[DataRequired(), Length(max=50)])
    innlegg = TextAreaField('Innlegg: ', validators=[DataRequired(), Length(max=6000)])  # cirka 2 sider
    tag = SelectMultipleField(u'Tag: ', choices=selectTag)
    newTag = StringField('Ny tag: ', validators=[Length(max=10)])      # kan ikke være DataRequired(),
    # trenger vedlegg!
    bloggID = HiddenField()
    submit = SubmitField('Legg til')
