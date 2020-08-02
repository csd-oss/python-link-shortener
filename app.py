from flask import Flask, redirect
from db import urls

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<route>')
def redirect_user(route):
    doc = urls.find_one({"shortLink": route})
    return redirect(doc['redirectTo'])
