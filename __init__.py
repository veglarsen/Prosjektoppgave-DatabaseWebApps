from flask import Flask, render_template, request, redirect
from database import myDB
from blogg import Blogg

app = Flask(__name__, template_folder='templates')


@app.route('/')
def forside() -> 'html':
    with myDB() as db:
        result = db.selectBlogg()
    bloggObjektene = [Blogg(*x) for x in result]
    print(bloggObjektene)

    return render_template('index.html', bloggObjektene=bloggObjektene)


if __name__ == '__main__':
    app.run()