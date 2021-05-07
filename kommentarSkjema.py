from wtforms import Form, StringField, HiddenField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class NyKommentar(Form):
    innleggID = HiddenField()
    kommentar = StringField('Kommentar: ', validators=[DataRequired(), Length(max=200)])
    bruker = HiddenField()
    submit = SubmitField('Legg til')

class RedigerKommentar(Form):
    kommentarID = HiddenField()
    innleggID = HiddenField()
    kommentar = StringField('Kommentar: ', validators=[DataRequired(), Length(max=200)])
    # bruker = HiddenField()
    submit = SubmitField('Endre')