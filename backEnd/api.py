from flask import Flask

app = Flask(__name__)


@app.route('/api', methods={'GET'})
def api():
    return {
        'userId': 1,
        'title': "App Corrector"
    }


@app.route('/fun', methods={'GET'})
def fun():
    return {1: "hola caracola"}


@app.route('/post', methods={'POST'})
def post():
    return {1: "prueba post"}
