# Public Imports
from flask import jsonify, make_response
from flask_restx import Resource, reqparse, inputs
import traceback

# Private Imports
from api import api

check_text_model = reqparse.RequestParser()

check_text_model.add_argument('text',
                              type=str, required=True,
                              help="Input text to check for hate speech")
check_text_model.add_argument('model', type=str, required=False,
                              default='xgboost', help="Model to be called")


class CheckText(Resource):
    @api.expect(check_text_model)
    def post(self):
        try:
            args = check_text_model.parse_args()
            text = args['text']
            model = args['model']

            return text

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in CheckText POST"}
            return make_response(jsonify(error_json), 500)
