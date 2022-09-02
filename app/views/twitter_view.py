# Public Imports
from flask import jsonify, make_response
from flask_restx import Resource, reqparse
import traceback
from dateutil.parser import parse

# Private Imports
from api import api
from config import MODEL_LIST, MODEL_PREDICTIONS
from src.twitter.twitter_scraping import condition_based_scraping
from src.utils.format_twitter_preds import format_predictions
from src.db.db_operations import insert_live_scraping, delete_live_scraping

MODEL_NAMES = [x["name"] for x in MODEL_LIST]
MODEL_NAMES.sort(reverse=True)

condition_based_model = reqparse.RequestParser()
condition_based_model.add_argument('username',
                                   type=str, required=True,
                                   help="Username of the twitter account")
condition_based_model.add_argument('model', type=str, required=True,
                                   default=MODEL_NAMES[0],
                                   help="Model to be called",
                                   choices=MODEL_NAMES)
condition_based_model.add_argument('start_date', type=str, required=False,
                                   help="Start date for checking tweets")
condition_based_model.add_argument('end_date', type=str, required=False,
                                   help="End date for checking tweets")

live_check_post_model = reqparse.RequestParser()
live_check_post_model.add_argument('username', type=str, required=True,
                                   help="Username of the twitter account")
live_check_post_model.add_argument('model', type=str, required=True,
                                   default=MODEL_NAMES[0],
                                   help="Model to be called",
                                   choices=MODEL_NAMES)
live_check_post_model.add_argument('action', type=str, required=True,
                                   default='start',
                                   help="Start or stop twitter scraping",
                                   choices=['start', 'stop'])

live_check_get_model = reqparse.RequestParser()
live_check_get_model.add_argument('username', type=str, required=True,
                                  help="Username of the twitter account")
live_check_get_model.add_argument('limit', type=int, required=False,
                                  default=20,
                                  help="No of results from live scraping")


class ConditionBased(Resource):
    @api.expect(condition_based_model)
    def post(self):
        try:
            args = condition_based_model.parse_args()
            username = args['username']
            model = args['model']
            raw_start_date = args['start_date']
            raw_end_date = args['end_date']

            if raw_start_date:
                try:
                    start_date = str(parse(raw_start_date))
                except ValueError:
                    return "Invalid start date", 400
            else:
                start_date = None

            if raw_end_date:
                try:
                    end_date = str(parse(raw_end_date))
                except ValueError:
                    return "Invalid end date", 400
            else:
                end_date = None

            model_details = [x for x in MODEL_LIST if x["name"] == model]
            if not model_details:
                return "Model not found", 400
            else:
                model_details = model_details[0]
            model_func = model_details["function"]
            model_config = model_details["config"]

            tweets, full_data = condition_based_scraping(username,
                                                         start_date=start_date,
                                                         end_date=end_date)

            predictions = model_func(input_text=tweets,
                                     model_config=model_config)

            result = format_predictions(full_data, predictions)

            return result.to_dict('records')

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in ConditionBased POST"}
            return make_response(jsonify(error_json), 500)


class LiveCheck(Resource):
    @api.expect(live_check_post_model)
    def post(self):
        try:
            args = live_check_post_model.parse_args()
            username = args['username']
            action = args['action']
            model = args['model']

            if action == 'start':
                db_response, status_code = insert_live_scraping(username, model)
                return db_response, status_code
            else:
                db_response, status_code = delete_live_scraping(username, model)
                return db_response, status_code

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in LiveCheck POST"}
            return make_response(jsonify(error_json), 500)

    @api.expect(live_check_get_model)
    def get(self):
        try:
            args = live_check_get_model.parse_args()
            username = args['username']
            limit = args['limit']

            return []

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            error_json = {"Error": "Error in LiveCheck GET"}
            return make_response(jsonify(error_json), 500)
