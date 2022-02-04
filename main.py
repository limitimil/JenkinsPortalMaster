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
from jira_services.issue_transition_executor import *

_PATH = os.path.dirname(os.path.abspath(__file__))
_PATH = os.path.join(_PATH, 'logging.ini')
DEFAULT_LOG_CONFIG = os.path.abspath(_PATH)

logging.config.fileConfig(DEFAULT_LOG_CONFIG)
logger2 = logging.getLogger('flask')

app = Flask(__name__)
app.config['CORS_EXPOSE_HEADERS'] = 'Content-Disposition'
CORS(app)

@app.route('/append_comment/change_log', methods=['PUT'])
def change_log():
    params = request.json
    append_change_log( ** params)
    return 'OK', 200
    

@app.route('/append_comment/ci_reference', methods=['PUT'])
def ci_reference():
    append_ci_reference(** request.json)
    return 'OK', 200

@app.route('/append_comment/CI', methods=['PUT'])
def append_ci_with_link():
    params = request.json
    params.update({'customized_title': 'CI'})
    ca = CommentAppender(params['issue_key'])
    ca.aggregate_by_title(params['customized_title'])
    ca.append_url_references(params['reference_url'], params['customized_title'])
    return 'OK', 200

@app.route('/append_comment/<title>', methods=['PUT'])
def append_comment_with_link(title):
    params = request.json
    params.update({'customized_title': title})
    append_url_references(** params)
    return 'OK', 200

@app.route('/append/pr_line_up_message', methods=['PUT'])
def append_pr_line_up_message():
    msg = (
        "\n"
        "{panel:bgColor=#fffae6}\n"
        "在 teams 中排隊等待過PR \n"
        "https://teams.microsoft.com/_?tenantId=9c5df620-ac96-4343-883d-e2fac493dcc0#/conversations/UAT%20PR%20review?groupId=1cee8eb1-7bce-403d-9618-7e57ccf6bab8&threadId=19:32bcf5a38d764e32a44a220f4ac79501@thread.skype&ctx=channel\n"
        "{panel}\n"
    )
    params = request.json
    ca = CommentAppender(params['issue_key'])
    ca.push_message_to_the_last_comment(msg)
    return 'OK', 200

@app.route('/transition/verification', methods=['PUT'])
def transit_to_verification():
    params = request.json
    ite = IssueTransitionExecutor(params['issue_key'])
    ite.transit_to_default_verifier()
    return 'OK', 200

@app.route('/pass_bug_to_black_hole', methods=['PUT'])
def pass_bug_to_black_hole():
    FIX_COMMENT = '請 [~accountid:557058:1f244781-5557-4ab3-937e-d162614eccf2] 協助安排議題至適當時機/人員' # TODO: should be refactor
    params = request.json
    jira.add_comment(params['issue_key'], FIX_COMMENT)
    jira.issue(params['issue_key']).update(assignee= {'accountId': '557058:1f244781-5557-4ab3-937e-d162614eccf2'})
    return 'OK', 200

@app.route('/brief/<issue_key>', methods=['GET'])
def issue_brief(issue_key):
    ig = IssueGrabber(issue_key)
    return ig.toJSON()


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    logger2.error('%s', str(e))
    return jsonify(error=str(e)), code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
