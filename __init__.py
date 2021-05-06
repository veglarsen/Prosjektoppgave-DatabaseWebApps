import secrets
from datetime import date

from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from bruker import Bruker
from flask import Flask, render_template, request, redirect, session, make_response, url_for
from brukerSkjema import BrukerSkjema, loggInn, NyBrukerSkjema, RedigerInnleggForm
from database import myDB
from fileoperations import fileDB
from blogg import Blogg, Innlegg, Kommentar, Vedlegg, Tag
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

from innleggSkjema import NyttInnlegg
from kommentarSkjema import NyKommentar

app = Flask(__name__, template_folder='templates')




app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg', 'zip'}

app.secret_key = secrets.token_urlsafe(16)
csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    user_dict = session['bruker']
    bruker = Bruker(user_dict['id'], user_dict['bruker'], user_dict['etternavn'], user_dict['fornavn'],  user_dict['passwordHash'],  user_dict['eMail'])
    Bruker.isauthenticated = user_dict['is_authenticated']
    return bruker

@login_manager.unauthorized_handler
def unauthorized_callback():
       return redirect(url_for('login'))

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
            return render_template('index.html', bloggObjektene=bloggObjektene)

@app.route('/blogg')
def blogg() -> 'html':
    with myDB() as db:
        is_owner = False
        id = request.args.get('id')
        result = db.selectAlleInnlegg(id)
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            if current_user.is_authenticated:
                innleggData = Innlegg(*db.selectEtInnlegg(id))
                is_owner = Bruker.is_owner(current_user.bruker, current_user.bruker, innleggData.eier)
            innleggData = [Innlegg(*x) for x in result]
            blogg_navn = innleggData[0].blogg_navn
            blogg_ID = innleggData[0].blogg_ID
            return render_template('blogg.html', innleggData=innleggData, is_owner=is_owner, blogg_ID=blogg_ID, blogg_navn=blogg_navn)

@app.route('/innlegg')
def innlegg() -> 'html':
    with myDB() as db:
        id = request.args.get('id')
        db.incrementTreff(id)
        result = db.selectEtInnlegg(id)
        form = NyKommentar(request.form)
        if result is None:
            return render_template('error.html', msg='Invalid parameter')
        else:
            is_owner = False
            with myDB() as db:
                innleggData = Innlegg(*db.selectEtInnlegg(id))
                tag = db.selectTags(id)
                tagData = [Tag(*x) for x in tag]
            if current_user.is_authenticated:
                is_owner = Bruker.is_owner(current_user.bruker, current_user.bruker, innleggData.eier)
            with myDB() as db:
                kommentar = db.kommentarer(id)
                kommentarData = [Kommentar(*x) for x in kommentar]
            with fileDB() as filedb:
                result = filedb.selectAllVedlegg(id)
                alleVedlegg = [Vedlegg(*x) for x in result]
                blogg_navn = innleggData.blogg_navn
            return render_template('innlegg.html', innleggData=innleggData, kommentarData=kommentarData, is_owner=is_owner, blogg_navn=blogg_navn, attachments=alleVedlegg, tagData=tagData, form=form)

@app.route('/tagInnlegg')
def tagInnlegg() -> 'html':
    with myDB() as db:
        tag = request.args.get('tag')
        result = db.selectAlleInnleggTag(tag)
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            innleggData = [Innlegg(*x) for x in result]
            blogg_navn = innleggData[0].blogg_navn
            blogg_ID = innleggData[0].blogg_ID
            return render_template('blogg.html', innleggData=innleggData, blogg_ID=blogg_ID,
                                   blogg_navn=blogg_navn)


# @app.route('/login', methods=["GET", "POST"])
@app.route('/loggInn', methods=["GET", "POST"])
def login() -> 'html':
    form = loggInn(request.form)
    if request.method == "POST" and form.validate():
        pass
        bruker_navn = form.brukernavn.data
        passord = form.passord.data
        # bruker_navn = request.form['username']
        # password = request.form['password']

        with myDB() as db:
            aktuellBruker = Bruker(*db.selectBruker(bruker_navn))
            if Bruker.check_password(aktuellBruker, passord):
                print("Passordet er korrekt")
                aktuellBruker.is_authenticated = True
                login_user(aktuellBruker)
                session['bruker'] = aktuellBruker.__dict__
                print(session['bruker'])
                print(current_user.bruker)
                print(aktuellBruker.is_authenticated)
                return redirect('/admin')
            else:
                return render_template('loggInn.html', form=form)
    else:
        return render_template('loggInn.html', form=form)

@app.route('/admin', methods=["GET", "POST"])
@login_required
def admin() -> 'html':
    return redirect('/')

    # return render_template('admin.html', the_title="Bestkyttet side", user=current_user.bruker)
                                                                # login required
@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout() -> 'html':
    logout_user()
    return redirect('/')


@app.route('/nyBruker', methods=["GET", "POST"])
def nyBruker() -> 'html':
    form = NyBrukerSkjema(request.form)
    if request.method == "POST" and form.validate():

        brukernavn = form.brukernavn.data
        fornavn = form.fornavn.data
        etternavn = form.etternavn.data
        eMail = form.eMail.data
        passord = form.password.data
        hashedPassword = generate_password_hash(passord)
        bruker = (brukernavn, etternavn, fornavn, hashedPassword, eMail)
        with myDB() as db:
            db.addBruker(bruker)
        return redirect('/')
    else:
        return render_template('nyBruker.html', form=form)


@app.route('/brukerEndre', methods=["GET", "POST"])
@login_required
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

@app.route('/upload_page/<id>', methods=["GET", "POST"])
def upload_page(id) -> 'html':
    with fileDB() as db:
        result = db.selectAllVedlegg(id)
        if result:
            alleVedlegg = [Vedlegg(*x) for x in result]
            return render_template('upload.html', attachments=alleVedlegg)
        else:
            return render_template('upload.html', attachments=None, innlegg_id=id)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadfile/<id>', methods=['GET', 'POST'])
def upload_file(id):
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

        filename = secure_filename(file.filename)
        attachment = (filename, mimetype, blob, size, id)
        with fileDB() as db:
            db.addVedlegg(attachment)

        return redirect(url_for('forside', _external=True))
    else:
        return redirect(url_for('forside', _external=True))

@app.route('/download/<id>')
def download_file(id):
    with fileDB() as db:
        attachment = Vedlegg(*db.getVedlegg(id))
    if attachment is None:
            pass
    else:
        response = make_response(attachment.fil_data)
        response.headers.set('Content-Type', attachment.fil_type)
        response.headers.set('Content-Length', attachment.size)
        response.headers.set(
        'Content-Disposition', 'inline', filename = attachment.fil_navn)
        return response

@app.route('/bekreftSletting', methods=["GET", "POST"])
@login_required
def bekreftSletting() -> 'html':
    id = request.args.get('id')
    if not id:
        return render_template('error.html', msg='Invalid parameter')
    else:
        with myDB() as db:
            innlegget = db.selectEtInnlegg(id)
            if innlegget is None:
                return render_template('error.html', msg='Invalid parameter')
            else:
                innlegget = Innlegg(*innlegget)
                return render_template('bekreftSletting.html', innlegg=innlegget)

@app.route('/slettInnlegg', methods=["GET", "POST"])
@login_required
def slettInnlegg() -> 'html':
    if request.method == "POST":
        id = request.form['id']
        with fileDB() as db:
            db.slettInnlegg(id)
        return redirect('/')

    return redirect(url_for('forside'))


@app.route('/redigerInnlegg', methods=["GET", "POST"])
@login_required
def redigerInnlegg() -> 'html':
    form = RedigerInnleggForm(request.form)
    if request.method == "POST" and form.validate():
        # tegs = form.tegs.data
        id = request.form['id']
        tittel = form.tittel.data
        ingress = form.ingress.data
        innlegg = form.innlegg.data
        redigertInnlegg = (innlegg, tittel, ingress, id)
        with myDB() as db:
            result = db.redigerInnlegg(redigertInnlegg)
        return redirect('/')
    else:
        id = request.args.get('id')
        with myDB() as db:
            innlegget = db.selectEtInnlegg(id)
            innleggObj = Innlegg(*innlegget)
            form = RedigerInnleggForm(request.form)
            form.id.data = innleggObj.innlegg_ID
            form.tittel.data = innleggObj.tittel
            form.ingress.data = innleggObj.ingress
            form.innlegg.data = innleggObj.innlegg

            if id:
                with fileDB() as filedb:
                    result = filedb.selectAllVedlegg(id)
                    alleVedlegg = [Vedlegg(*x) for x in result]

                    return render_template('redigerInnlegg.html', form=form, attachments=alleVedlegg)

            return render_template('redigerInnlegg.html', form=form)

@app.route('/tegneNyttInnlegg', methods=["GET", "POST"])
def tegneNyttInnlegg() -> 'html':
    form = NyttInnlegg()
    form.bloggID.data = request.args.get('id')
    # with fileDB() as db:
    #     result = db.selectAllVedlegg()
    #     alleVedlegg = [Vedlegg(*x) for x in result]
    return render_template('nyttInnlegg.html', form=form)


@app.route('/add', methods=["GET", "POST"])
@login_required
def nyttInnlegg() -> 'html':
    form = NyttInnlegg(request.form)
    if request.method == "POST" and form.validate():
        # tror ikke innleggID er nødvendig
        bloggID = form.bloggID.data
        tittel = form.tittel.data
        ingress = form.ingress.data
        innlegg = form.innlegg.data
        tag = form.tag.data  # if null use newTag
        newTag = form.newTag.data  # if null, use tag

        nyttInnlegg = (bloggID, tittel, ingress, innlegg)

        with myDB() as db:
            lastID = db.nyttInnlegg(nyttInnlegg, tag, newTag)
            return redirect(url_for('upload_page', id=lastID))

            db.nyttInnlegg(nyttInnlegg, tag, newTag)
        return redirect('/')
    else:
        return render_template('nyttInnlegg.html', form=form)

@app.route('/nyKommentar', methods=["GET", "POST"])
@login_required
def nyKommentar() -> 'html':
    form = NyKommentar(request.form)
    if request.method == "POST" and form.validate():
        innleggID = form.innleggID.data
        bruker = current_user.bruker
        kommentar = form.kommentar.data
        kommentarSQL = (innleggID, innleggID, bruker, kommentar)
        with myDB() as db:
            db.nyKommentar(kommentarSQL)
        return redirect(url_for("innlegg", id=innleggID))
    else:
        return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
