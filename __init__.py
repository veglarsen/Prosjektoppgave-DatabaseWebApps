from flask import Flask, render_template, request, redirect
from database import myDB
from blogg import Blogg, Innlegg

app = Flask(__name__, template_folder='templates')


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
            return render_template('blogg.html', innleggData=innleggData)


if __name__ == '__main__':
    app.run()
