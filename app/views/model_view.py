# Public Imports
from flask import jsonify, make_response
from flask_restx import Resource, reqparse, inputs
import traceback

# Private Imports
from config import MODEL_LIST


class ShowModels(Resource):
    def get(self):
        try:
            model_names = [x["name"] for x in MODEL_LIST]
            return model_names

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in ShowModels GET"}
            return make_response(jsonify(error_json), 500)
