from flask import Flask, redirect, request, jsonify
from pymongo.errors import DuplicateKeyError
import requests
import json

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
    try:
        url = doc['callbackUrl']
        doc['_id'] = str(doc['_id'])
        headers = {'content-type': 'application/json'}
        requests.request(
            "POST", url, data=json.dumps(doc), headers=headers
            )
        return redirect(doc['redirectTo'])
    except KeyError:
        return redirect(doc['redirectTo'])


class Error(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(Error)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/addShortLink', methods=['POST'])
def add_short_link():
    doc = request.get_json()
    try:
        urls.insert_one(doc)
        return doc
    except DuplicateKeyError:
        raise Error("not unique short id", status_code=409)
