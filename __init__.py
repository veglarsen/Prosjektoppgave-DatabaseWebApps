import secrets

from flask import Flask, render_template, request, redirect,session
from database import myDB
from blogg import Blogg, Innlegg, Kommentar, Bruker
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

app = Flask(__name__, template_folder='templates')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user_dict = session['user']
    user = Bruker(user_dict['id'], user_dict['passwordHash'], user_dict['firstname'], user_dict['lastname'], user_dict['username'])
    user.isauthenticated = user_dict['is_authenticated']

@app.route('hemmelig')
@login_required
def hemmelig() -> 'html':
    return render_template('hemmelig.html', the_title="Bestkyttet side")

@app.route('/')
def forside() -> 'html':
    with myDB() as db:
        result = db.selectBlogg()
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            bloggObjektene = [Blogg(*x) for x in result]
            print(bloggObjektene)
            return render_template('index.html', bloggObjektene=bloggObjektene)

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
    if request.method == "POST":

        bruker_navn = request.form['username']
        password = request.form['password']
        with Bruker() as bruker:
            aktuellBruker = Bruker(*bruker.selectBruker(bruker_navn))
            if bruker.check_password(password):
                aktuellBruker.is_authenticated = True
                login_user(aktuellBruker)
                session['user'] = aktuellBruker.__dict__

        return redirect('/')

@app.route('/logout', methods=["GET", "POST"])

def logout() -> 'html':
    session.pop('logged_in')
    return redirect('/')

app.secret_key = secrets.token_urlsafe(16)

if __name__ == '__main__':
    app.run()
