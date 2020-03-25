from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
# import app

class KlausimasForm(FlaskForm):
    klausimas = StringField('Klausimas', [DataRequired()])
    pirmas_atsakymas = StringField('1 atsakymas', [DataRequired()])
    antras_atsakymas = StringField('2 atsakymas', [DataRequired()])
    trecias_atsakymas = StringField('3 atsakymas', [DataRequired()])
    submit = SubmitField('Įvesti')

class TestasForm(FlaskForm):
    pirmas_atsakymas = BooleanField('1 atsakymas')
    antras_atsakymas = BooleanField('2 atsakymas')
    trecias_atsakymas = BooleanField('3 atsakymas')
    submit = SubmitField('Kitas klausimas')
