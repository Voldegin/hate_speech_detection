# Public Imports
from flask import jsonify, make_response
from flask_restx import Resource, reqparse, inputs
import traceback

# Private Imports
from api import api
from config import MODEL_LIST, MODEL_PREDICTIONS

MODEL_NAMES = [x["name"] for x in MODEL_LIST]
MODEL_NAMES.sort(reverse=True)

check_text_model = reqparse.RequestParser()

check_text_model.add_argument('text',
                              type=str, required=True,
                              help="Input text to check for hate speech")
check_text_model.add_argument('model', type=str, required=True,
                              default=MODEL_NAMES[0], help="Model to be called",
                              choices=MODEL_NAMES)


class CheckText(Resource):
    @api.expect(check_text_model)
    def post(self):
        try:
            args = check_text_model.parse_args()
            text = args['text']
            model = args['model']

            model_details = [x for x in MODEL_LIST if x["name"] == model]
            if not model_details:
                return "Model not found", 400
            else:
                model_details = model_details[0]
            model_func = model_details["function"]
            model_config = model_details["config"]

            a = model_func(input_text=text, model_config=model_config)
            print(a)
            prediction = a[0]

            return MODEL_PREDICTIONS[prediction]

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in CheckText POST"}
            return make_response(jsonify(error_json), 500)
