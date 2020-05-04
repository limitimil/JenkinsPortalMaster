# -*- coding: utf-8 -*-
import requests
from flask import jsonify
from flask_cors import CORS
from flask import Flask
from flask import request

from werkzeug.exceptions import HTTPException

import os
import logging
import logging.config

from jira_services.comments_appender import *
from socketio.core import helloworld

_PATH = os.path.dirname(os.path.abspath(__file__))
_PATH = os.path.join(_PATH, 'logging.ini')
DEFAULT_LOG_CONFIG = os.path.abspath(_PATH)

logging.config.fileConfig(DEFAULT_LOG_CONFIG)
logger2 = logging.getLogger('flask')

app = Flask(__name__)
app.config['CORS_EXPOSE_HEADERS'] = 'Content-Disposition'
CORS(app)

@app.route('/append_comment/ci_reference', methods=['PUT'])
def ci_reference():
    append_ci_reference(** request.json)
    return 'OK', 200

@app.route('/append_comment/<title>', methods=['PUT'])
def append_comment_with_link(title):
    params = request.json
    params.update({'customized_title': title})
    append_url_references(** params)
    return 'OK', 200

@app.route('/hello/socketio/', methods=['GET'])
def hello_socketio():
    helloworld()
    return 'You should wait for hello from soket io', 200



@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    logger2.error('%s', str(e))
    return jsonify(error=str(e)), code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
