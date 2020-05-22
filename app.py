import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'testai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Klausimas(db.Model):
    __tablename__ = "klausimas"
    id = db.Column(db.Integer, primary_key=True)
    klausimas = db.Column("Klausimas", db.String)
    pirmas_atsakymas = db.Column("1 atsakymas", db.String)
    antras_atsakymas = db.Column("2 atsakymas", db.String)
    trecias_atsakymas = db.Column("3 atsakymas", db.String)

class Atsakymas(db.Model):
    __tablename__ = "atsakymas"
    id = db.Column(db.Integer, primary_key=True)
    klausimo_id = db.Column("Klausimo ID", db.Integer)
    pirmas_atsakymas = db.Column("1 atsakymas", db.Boolean)
    antras_atsakymas = db.Column("2 atsakymas", db.Boolean)
    trecias_atsakymas = db.Column("3 atsakymas", db.Boolean)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/klausimai")
def klausimai():
    try:
        visi_klausimai = Klausimas.query.all()
    except:
        visi_klausimai = []
    return render_template("klausimai.html", visi_klausimai=visi_klausimai)

@app.route("/naujas_klausimas", methods=["GET", "POST"])
def naujas_klausimas():
    db.create_all()
    forma = forms.KlausimasForm()
    if forma.validate_on_submit():
        naujas_klausimas = Klausimas(klausimas=forma.klausimas.data, pirmas_atsakymas=forma.pirmas_atsakymas.data, antras_atsakymas=forma.antras_atsakymas.data, trecias_atsakymas=forma.trecias_atsakymas.data)
        db.session.add(naujas_klausimas)
        db.session.commit()
        return redirect(url_for('klausimai'))
    return render_template("prideti_klausima.html", form=forma)

@app.route("/testas", methods=["GET", "POST"])
@app.route("/testas/<int:klausimo_id>", methods=["GET", "POST"])
def testas(klausimo_id=0):
    db.create_all()
    forma = forms.TestasForm()
    klausimo_id += 1
    if klausimo_id <= len(Klausimas.query.all()):
        aktyvus_klausimas = Klausimas.query.get(klausimo_id)
        if forma.submit():
            atsakymas = Atsakymas(klausimo_id=aktyvus_klausimas.id, pirmas_atsakymas=forma.pirmas_atsakymas.data, antras_atsakymas=forma.antras_atsakymas.data, trecias_atsakymas=forma.trecias_atsakymas.data)
            db.session.add(atsakymas)
            db.session.commit()
            return render_template("testas.html", form=forma, aktyvus_klausimas=aktyvus_klausimas)
    else:
        return "Testas baigtas"
    return render_template("testas.html", form=forma, aktyvus_klausimas=aktyvus_klausimas)

@app.route("/istrinti_klausima/<int:id>")
def istrinti_klausima(id):
    uzklausa = Klausimas.query.get(id)
    db.session.delete(uzklausa)
    db.session.commit()
    return redirect(url_for('klausimai'))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    db.create_all()