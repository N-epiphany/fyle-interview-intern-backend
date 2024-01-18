# file: responses.py path: core/apis/responses.py
# Description: This file contains the APIResponse class

from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))
    @classmethod
    def respond_error(cls, status_code):
        return make_response(jsonify(error="Error"), status_code)
