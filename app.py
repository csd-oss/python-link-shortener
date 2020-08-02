from flask import Flask, redirect
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


doc = {
    "originalLink": "https://github.com/csd-oss/python-link-shortener",
    "redirectTo": "https://github.com/csd-oss/python-link-shortener"
}


@app.route('/<route>')
def show_user_profile(route):
    return redirect(doc['redirectTo'])
