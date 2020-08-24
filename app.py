import json
import time
from random import randint

import requests
import short_url
from flask import Flask, jsonify, redirect, request
from pymongo.errors import DuplicateKeyError

from db import urls
from device_parser import device_parser
from mongoflask import MongoJSONEncoder, ObjectIdConverter

app = Flask(__name__)
app.json_encoder = MongoJSONEncoder
app.url_map.converters['objectid'] = ObjectIdConverter


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


@app.route('/')
def hello_world():
    return 'Hello, World!'


def send_callbak(callbackUrl, data):
    headers = {'content-type': 'application/json'}
    requests.request(
        "POST", callbackUrl, data=json.dumps(data), headers=headers
    )


@app.route('/<route>')
def redirect_user(route):
    doc = urls.find_one({"shortLink": route})
    try:
        url = doc['callbackUrl']
        doc['_id'] = str(doc['_id'])

        doc['timestamp'] = time.time()
        doc['userAgent'] = request.headers.get('User-Agent')
        doc['device'] = device_parser(doc['userAgent'])
        send_callbak(url, doc)
        return redirect(doc['redirectTo'])
    except KeyError:
        return redirect(doc['redirectTo'])
    except TypeError:
        raise Error("No link found",   status_code=404)


# TODO Web interface for adding links
@app.route('/addShortLink', methods=['POST', 'GET'])
def add_short_link():
    doc = request.get_json()
    if 'redirectTo' not in doc:
        raise Error(
            "The required parameter 'redirectTo' is missing",
            status_code=400
            )
    else:
        # TODO Refactor this to make it more undestandable
        try:
            try:
                if ('shortLink' in doc) & (doc['shortLink'] != ""):
                    urls.insert_one(doc)
                    return doc
                elif doc['shortLink'] == "":
                    block_size = randint(0, 100000000)
                    doc['shortLink'] = short_url.encode_url(block_size)
                    urls.insert_one(doc)
                    return doc
            except KeyError:
                block_size = randint(0, 100000000)
                doc['shortLink'] = short_url.encode_url(block_size)
                urls.insert_one(doc)
                return doc
        except DuplicateKeyError:
            raise Error("Not unique shortId", status_code=409)


if __name__ == "__main__":
    app.run()
