from flask import Flask, redirect, request
from db import urls

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/<route>')
def redirect_user(route):
    doc = urls.find_one({"shortLink": route})
    return redirect(doc['redirectTo'])


@app.route('/addShortLink', methods=['POST'])
def add_short_link():
    doc = request.get_json()
    urls.insert_one(doc)
    return doc
