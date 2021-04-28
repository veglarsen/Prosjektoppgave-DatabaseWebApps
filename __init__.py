import secrets
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash
from bruker import Bruker
from flask import Flask, render_template, request, redirect

from brukerSkjema import BrukerSkjema
from database import myDB
from blogg import Blogg, Innlegg, Kommentar
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_dict = session['bruker']
    bruker = Bruker(user_dict['id'], user_dict['bruker'], user_dict['etternavn'], user_dict['fornavn'],  user_dict['passwordHash'],  user_dict['eMail'])
    bruker.isauthenticated = user_dict['is_authenticated']
    return bruker

@app.route('/')
def forside() -> 'html':
    print("Forside")
    redirect('/login')
    with myDB() as db:
        result = db.selectBlogg()
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            bloggObjektene = [Blogg(*x) for x in result]
            print(bloggObjektene)
            return render_template('index.html', bloggObjektene=bloggObjektene)

@app.route('/hemmelig')
@login_required
def hemmelig() -> 'html':
    # if 'logged_in' in session:
    return render_template('hemmelig.html', the_title="Bestkyttet side")
    # else:
    #     return redirect("/")

@app.route('/blogg')
def blogg() -> 'html':
    with myDB() as db:
        id = request.args.get('id')
        result = db.selectAlleInnlegg(id)
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            innleggData = [Innlegg(*x) for x in result]
            return render_template('blogg.html', innleggData=innleggData)

@app.route('/innlegg')
def innlegg() -> 'html':
    with myDB() as db:
        id = request.args.get('id')
        db.incrementTreff(id)
        result = db.selectEtInnlegg(id)
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            innleggData = [Innlegg(*x) for x in result]
            kommentar = db.kommentarer(id)
            kommentarData = [Kommentar(*x) for x in kommentar]
            return render_template('innlegg.html', innleggData=innleggData, kommentarData=kommentarData)

@app.route('/login', methods=["GET", "POST"])
def login() -> 'html':
    if request.method == "GET":                 #POST
        # bruker_navn = request.form['username']
        # password = request.form['password']
        bruker_navn = "bruker_en"
        passord = "passord"
        # if Bruker.login(bruker_navn, passord):
        #     session['logged_in'] = True
        #     session['username'] = bruker_navn
        #     flash('You are logged in')
        #     return redirect('/hemmelig')
        # return redirect('/')

        with myDB() as db:
            aktuellBruker = Bruker(*db.selectBruker(bruker_navn))
            if Bruker.check_password(aktuellBruker, passord):
                print("Passordet er korrekt")
                aktuellBruker.is_authenticated = True
                login_user(aktuellBruker)
                session['bruker'] = aktuellBruker.__dict__
                print(session['bruker'])
            return redirect('/hemmelig')

@app.route('/logout', methods=["GET", "POST"])

def logout() -> 'html':
    session.pop('logged_in')
    return redirect('/')

app.secret_key = secrets.token_urlsafe(16)
@app.route('/brukerEndre', methods=["GET", "POST"])
def brukerEndre() -> 'html':
    form = BrukerSkjema(request.form)
    if request.method == "POST" and form.validate():

        brukernavn = request.form['brukernavn']
        fornavn = form.fornavn.data
        etternavn = form.etternavn.data
        eMail = form.eMail.data
        bruker = (fornavn, etternavn, eMail, brukernavn)
        with myDB() as db:
            result = db.brukerEndre(bruker)
        return redirect('/')
    else:
        return render_template('brukerEndre.html',
                               form=form)

if __name__ == '__main__':
    app.run()
