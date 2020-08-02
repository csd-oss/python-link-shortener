from flask import Flask, redirect, request
from pymongo.errors import DuplicateKeyError

from db import urls
from mongoflask import MongoJSONEncoder, ObjectIdConverter

app = Flask(__name__)
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter


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
    try:
        urls.insert_one(doc)
    except DuplicateKeyError:
        doc = {
            "error": "not unique short id"
        }
    return doc
