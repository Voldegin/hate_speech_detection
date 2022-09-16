# Public Imports
from flask import jsonify, make_response
from flask_restx import Resource, reqparse, inputs
import traceback

# Private Imports
from config import MODEL_LIST
from log import logger


class ShowModels(Resource):
    def get(self):
        try:
            # Show all Model names
            model_names = [x["name"] for x in MODEL_LIST]
            return model_names

        except Exception as e:
            logger.error(e)
            logger.info(traceback.format_exc())
            error_json = {"Error": "Error in ShowModels GET"}
            return make_response(jsonify(error_json), 500)
