import secrets
from datetime import date

from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from bruker import Bruker
from flask import Flask, render_template, request, redirect, session, make_response, url_for
from brukerSkjema import BrukerSkjema, loggInn, NyBrukerSkjema
from database import myDB
from fileoperations import fileDB
from blogg import Blogg, Innlegg, Kommentar, Vedlegg, Tag, InnleggTag
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
from innleggSkjema import NyttInnlegg, SearchForm, RedigerInnleggForm, NyBlogg
from kommentarSkjema import NyKommentar, RedigerKommentar

app = Flask(__name__, template_folder='templates')




app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'ogg'}

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
    searchForm = SearchForm(request.form)
    redirect('/login')
    with myDB() as db:
        result = db.selectBlogg()
        tags = db.selectTag()
        searchForm.tag.choices = [(tag[0], tag[1]) for tag in tags]

        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            bloggObjektene = [Blogg(*x) for x in result]
            return render_template('index.html', bloggObjektene=bloggObjektene, searchForm=searchForm)

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
            bloggData = db.selectEnBlogg(id)
            bloggDataUt = Blogg(*bloggData)
            # bloggDataUt = [Blogg(*x) for x in bloggData]

            if current_user.is_authenticated:
                is_owner = Bruker.is_owner(current_user.bruker, current_user.bruker, bloggDataUt.eier)
            innleggData = [Innlegg(*x) for x in result]
            blogg_navn = bloggDataUt.blogg_navn
            blogg_ID = bloggDataUt.blogg_ID

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
            innleggData = [InnleggTag(*x) for x in result]
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
            brukeren = db.selectBruker(bruker_navn)
            if brukeren != None:
                aktuellBruker = Bruker(*brukeren)
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
                return render_template('loggInn.html', form=form, brukerFinnes=False)
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

# @app.route('/upload_page/<id>', methods=["GET", "POST"])
# def upload_page(id) -> 'html':
#     with fileDB() as db:
#         result = db.selectAllVedlegg(id)
#         if result:
#             alleVedlegg = [Vedlegg(*x) for x in result]
#             return render_template('upload.html', attachments=alleVedlegg)
#         else:
#             return render_template('upload.html', attachments=None, innlegg_id=id)

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

        return redirect(url_for('innlegg', id=id, _external=True))
    else:
        return redirect(url_for('forside', id=id, _external=True))

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

@app.route('/delete/<id>/<vedleggID>')
def delete_file(id, vedleggID):

    with fileDB() as filedb:
        filedb.slettVedlegg(id, vedleggID)
    return redirect(url_for('innlegg', id=id))


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
        blogg_id = request.form['blogg_id']
        with fileDB() as db:
            db.slettInnlegg(id)
        return redirect(url_for('blogg', id=blogg_id))

    return redirect(url_for('forside'))


@app.route('/redigerInnlegg', methods=["GET", "POST"])
@login_required
def redigerInnlegg() -> 'html':
    form = RedigerInnleggForm(request.form)
    with myDB() as db:
        tags = db.selectTag()
    form.tag.choices = [(tag[0], tag[1]) for tag in tags]

    if request.method == "POST" and form.validate():
        id = request.form['id']
        tittel = form.tittel.data
        ingress = form.ingress.data
        innlegg = form.innlegg.data
        nytag = form.newTag.data

        redigertInnlegg = (innlegg, tittel, ingress, id)
        with myDB() as db:
            db.redigerInnlegg(redigertInnlegg)

            oldTagID = db.selectTags(id)
            innlegg_innlegg_ID = id
            tag_tag_ID = form.tag.data

            if db.boolean_validate_tag_navn(nytag) and nytag !='':
                db.createNewTag(nytag)
                nytagID = db.getLastAddedTagID()
                tag_tag_ID.append(nytagID)

            # Hvis ingen tag er valgt, velger tag 1 (udef.)
            if tag_tag_ID == []:
                tag_tag_ID = [1];
            innlegg_blogg_ID = db.currentBloggID(id)

            # Hvis innlegget har en tag fra før, beholde forrige tag
            if len(tag_tag_ID) == 0 and len(oldTagID) == 1:
                tag_tag_ID = oldTagID[0]
                tagInnlegg = (tag_tag_ID, innlegg_innlegg_ID, innlegg_blogg_ID)
                # db.updateTagInnlegg(tagInnlegg)
                for tag in tag_tag_ID:
                    # db.updateTagInnlegg(tag, innlegg_innlegg_ID, innlegg_blogg_ID)
                    tagInnlegg = (tag, tag, innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.updateTagInnlegg(tagInnlegg)
                # db.updateTagInnlegg(tag_tag_ID, innlegg_innlegg_ID, innlegg_blogg_ID)

            # Hvis innlegget har like mange nye tags som gamle tags, oppdaterer til nye tags
            elif len(tag_tag_ID) == len(oldTagID):
                for i in range(0, len(tag_tag_ID)):
                    oldTag = oldTagID[i]
                    tagInnlegg = (tag_tag_ID[i], oldTag[0], innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.updateTagInnlegg(tagInnlegg)

            # Hvis det er færre nye tags enn gamle, så oppdateres ant gamle tags som nye, og resten fjernes
            elif len(tag_tag_ID) < len(oldTagID):
                for i in range(0, len(oldTagID) - (len(oldTagID) - len(tag_tag_ID))):
                    oldTag = oldTagID[i]
                    tagInnlegg = (tag_tag_ID[i], oldTag[0], innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.updateTagInnlegg(tagInnlegg)

                for j in range(len(oldTagID) - len(tag_tag_ID), 0, -1):
                    oldTag = oldTagID[j]
                    tagInnlegg = (oldTag[0], innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.deleteTagFromInnlegg(tagInnlegg)

            # Hvis det er flere nye tags en gamle, så oppdateres de gamle, og deretter legges de nye til
            elif len(tag_tag_ID) > len(oldTagID):
                for i in range(0, len(tag_tag_ID) - (len(tag_tag_ID) - len(oldTagID))):
                    oldTag = oldTagID[i]
                    tagInnlegg = (tag_tag_ID[i], oldTag[0], innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.updateTagInnlegg(tagInnlegg)

                for j in range(len(tag_tag_ID) - (len(tag_tag_ID) - len(oldTagID)), len(tag_tag_ID)):
                    tagInnlegg = (tag_tag_ID[j], innlegg_innlegg_ID, innlegg_blogg_ID[0])
                    db.addTagToInnlegg(tagInnlegg)

        return redirect(url_for("innlegg", id=innlegg_innlegg_ID))
    else:
        id = request.args.get('id')
        with myDB() as db:
            innlegget = db.selectEtInnlegg(id)
            innleggObj = Innlegg(*innlegget)
            form = RedigerInnleggForm(request.form)
            tags = db.selectTag()
            form.tag.choices = [(tag[0], tag[1]) for tag in tags]
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
    with myDB() as db:
        tags = db.selectTag();
    form = NyttInnlegg()
    form.tag.choices = [(tag[0], tag[1]) for tag in tags]
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
        tag = form.tag.data
        newTag = form.newTag.data

        nyttInnlegg = (bloggID, tittel, ingress, innlegg)

        with myDB() as db:
            lastID = db.nyttInnlegg(nyttInnlegg, tag, newTag)
            return redirect(url_for('redigerInnlegg', id=lastID))

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

@app.route('/redigerKommentar', methods=["GET", "POST"])
@login_required
def redigerKommentar() -> 'html':
    form = RedigerKommentar(request.form)
    if request.method == "POST" and form.validate():
        # bruker = current_user.bruker
        innlegg_ID = form.innlegg_ID.data # henter blank str
        kommentarID = request.form['kommentarID']
        kommentar = form.kommentar.data
        redigertKommentar = (kommentar, kommentarID)
        with myDB() as db:
            db.redigerKommentar(redigertKommentar)
        return redirect(url_for("innlegg", id=innlegg_ID))
    else:
        kommentarID = request.args.get('kommentarID')
        with myDB() as db:
            # innleggData = Innlegg(*db.selectEtInnlegg(kommentarID))
            kommentaren = db.selectEnKommentar(kommentarID)
            kommentarObj = Kommentar(*kommentaren)
            form = RedigerKommentar(request.form)
            form.kommentarID.data = kommentarObj.kommentar_ID
            form.kommentar.data = kommentarObj.kommentar
            form.innlegg_ID.data = kommentarObj.innlegg_ID
        return render_template('redigerKommentar.html', form=form)
        # return render_template('redigerKommentar.html', form=form, innlegg_ID=form.innleggID.data)

@app.route('/slettKommentar', methods=["GET", "POST"])
def slettKommentar() -> 'html':
    id = request.args.get('id')
    innleggID = request.args.get('innleggID')
    with myDB() as db:
        db.slettKommentar(id)
    return redirect(url_for("innlegg", id=innleggID))

@app.route('/search', methods=["GET", "POST"])
def search() -> 'html':
    searchForm = SearchForm()

    if request.method == "GET":
        searchKeyWord = request.args.get('searchField')
        searchTag = request.args.get('tag')
        with myDB() as db:
            if(searchKeyWord != "" and searchTag != None):
                result = db.searchAndTag(searchKeyWord, searchTag)
                innleggData = [Innlegg(*x) for x in result]
            elif(searchKeyWord == "" and searchTag != None):
                result = db.selectAlleInnleggTag(searchTag)
                innleggData = [InnleggTag(*x) for x in result]
            elif (searchKeyWord != "" and searchTag == None):
                result = db.search(searchKeyWord)
                innleggData = [Innlegg(*x) for x in result]
            elif (searchKeyWord == "" and searchTag == None):
                return redirect(url_for("forside"))
        if result is None:
            return render_template('error.html',
                                   msg='Invalid parameter')
        else:
            return render_template('blogg.html', innleggData=innleggData, searchForm=searchForm)
    return render_template('error.html', msg='Invalid parameter')

@login_required
@app.route('/nyBlogg', methods=["GET", "POST"])
def nyBlogg() -> 'html':
    form = NyBlogg(request.form)
    if request.method == "POST" and form.validate():
        eier = current_user.bruker
        blogg_navn = form.blogg_navn.data
        with myDB() as db:
            db.newBlogg(blogg_navn, eier)
        return redirect(url_for(forside))
    return render_template('nyBlogg.html', form=form)

@login_required
@app.route('/bekreftSlettingBlogg', methods=["GET", "POST"])
def bekreftSlettingBlogg() -> 'html':
    id = request.args.get('id')
    if not id:
        return render_template('error.html', msg='Invalid parameter')
    else:
        with myDB() as db:
            blogg = db.selectEnBlogg(id)
            if blogg is None:
                return render_template('error.html', msg='Invalid parameter')
            else:
                blogg2 = Blogg(*blogg)
                return render_template('bekreftSlettingBlogg.html', blogg=blogg2)

@app.route('/slettBlogg', methods=["GET", "POST"])
@login_required
def slettBlogg() -> 'html':
    if request.method == "POST":
        id = request.form['blogg_ID']
        with fileDB() as db:
            db.slettBlogg(id)
    else:
        print("test")
    return redirect(url_for('forside'))

if __name__ == '__main__':
    app.run(debug=True)