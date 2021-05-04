from wtforms import Form, StringField, HiddenField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class NyKommentar(Form):
    # må være innlogget
    innleggID = HiddenField()
    kommentar = StringField('Kommentar: ', validators=[DataRequired(), Length(max=200)])
    dato = DateField('Dato', validators=[DataRequired()])
    bruker = HiddenField()
    submit = SubmitField('Legg til')

class EndreKommentar(Form):
    innleggID = HiddenField()
    kommentar = StringField('Kommentar: ', validators=[DataRequired(), Length(max=200)])
    dato = DateField('Dato', validators=[DataRequired()])
    bruker = HiddenField()
    submit = SubmitField('Endre')