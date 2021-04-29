import secrets
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from bruker import Bruker
from flask import Flask, render_template, request, redirect, session, make_response, url_for
from brukerSkjema import BrukerSkjema, loggInn
from database import myDB
from blogg import Blogg, Innlegg, Kommentar, Vedlegg
from flask_login import LoginManager, current_user, login_user, logout_user, login_required


app = Flask(__name__, template_folder='templates')
# app.secret_key = b'_5#y2L"F4Q8z<\n\xec]/'             #??????????????????????
# csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg', 'zip'}
csrf = CSRFProtect(app)

@login_manager.user_loader
def load_user(user_id):
    user_dict = session['bruker']
    bruker = Bruker(user_dict['id'], user_dict['bruker'], user_dict['etternavn'], user_dict['fornavn'],  user_dict['passwordHash'],  user_dict['eMail'])
    bruker.isauthenticated = user_dict['is_authenticated']
    return bruker

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#        return redirect(url_for('login'))

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
    pass
    return render_template('hemmelig.html', the_title="Bestkyttet side")

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

# @app.route('/login', methods=["GET", "POST"])
@app.route('/loggInn', methods=["GET", "POST"])
def login() -> 'html':
    form = loggInn(request.form)
    if request.method == "POST" and form.validate():
        bruker_navn = form.brukernavn.data
        passord =  form.brukernavn.data
        # bruker = (brukernavn, passord)
    # if request.method == "GET":                 #POST
        # bruker_navn = request.form['username']
        # password = request.form['password']
        # bruker_navn = "bruker_en"
        # passord = "passord"
        if form.validate_on_submit():
            return '<h1>' + form.brukernavn.data + " " + form.passord.data + '</h1>'
        with myDB() as db:
            aktuellBruker = Bruker(*db.selectBruker(bruker_navn))
            if Bruker.check_password(aktuellBruker, passord):
                print("Passordet er korrekt")
                aktuellBruker.is_authenticated = True
                login_user(aktuellBruker)
                session['bruker'] = aktuellBruker.__dict__
                print(session['bruker'])
            return redirect('/hemmelig')
    else:
        return render_template('loggInn.html', form=form)


@app.route('/logout', methods=["GET", "POST"])

def logout() -> 'html':
    session.pop('logged_in')
    return redirect('/')


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


@app.route('/upload_page', methods=["GET", "POST"])
def upload_page() -> 'html':
    with myDB() as db:
        result = db.selectAllVedlegg()
        alleVedlegg = [Vedlegg(*x) for x in result]
        return render_template('upload.html', attachments=alleVedlegg)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return render_template('error.html',
                               msg='No files')
    file = request.files['file']
    mimetype = file.mimetype
    blob = request.files['file'].read()
    size = len(blob)

    if file.filename == '':
        print('no filename')
        return redirect(request.url)
    elif file and allowed_file(file.filename):
        id = 1
        filename = secure_filename(file.filename)
        attachment = (filename, mimetype, blob, size, id)
        with myDB() as db:
            result = db.addVedlegg(attachment)

        return redirect(url_for('show_all_files', _external=True))
    else:
        return redirect(url_for('show_all_files', _external=True))

@app.route('/download/<id>')
def download_file(id):
    with myDB() as db:
        attachment = Vedlegg(*db.get(id))
    if attachment is None:
            pass
    else:
        response = make_response(attachment.code)
        response.headers.set('Content-Type', attachment.mimetype)
        response.headers.set('Content-Length', attachment.size)
        response.headers.set(
        'Content-Disposition', 'inline', filename = attachment.filename)
        return response

app.secret_key = secrets.token_urlsafe(16)

if __name__ == '__main__':
    app.run(debug=True)
