# Public Imports
from flask_restx import Namespace
from flask import Blueprint

# Private Imports
from views.offline_view import CheckText
from views.model_view import ShowModels
from views.twitter_view import ConditionBased, LiveCheck
from api import api

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)

model_namespace = Namespace('models')
model_namespace.add_resource(ShowModels, '/all_models')

offline_namespace = Namespace('offline')
offline_namespace.add_resource(CheckText, '/check_text')

twitter_namespace = Namespace('twitter')
twitter_namespace.add_resource(ConditionBased, '/condition_based')
twitter_namespace.add_resource(LiveCheck, '/live_results')

api.add_namespace(model_namespace)
api.add_namespace(offline_namespace)
api.add_namespace(twitter_namespace)
