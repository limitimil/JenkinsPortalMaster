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

from jira_services.comments_appender import append_ci_reference

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


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    logger2.error('%s', str(e))
    return jsonify(error=str(e)), code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
