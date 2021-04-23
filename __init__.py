from flask import Flask, render_template, request, redirect
from database import myDB

app = Flask(__name__)


@app.route('/')
def forside() -> 'html':

    return render_template('index.html')


if __name__ == '__main__':
    app.run()