from flask import Flask, render_template, request, redirect
from database import myDB

app = Flask(__name__, template_folder='templates')


@app.route('/')
def forside() -> 'html':
    with myDB() as db:
        result = db.selectBlogg()

    return render_template('index.html', blogg=result)


if __name__ == '__main__':
    app.run()