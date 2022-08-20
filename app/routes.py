# Public Imports
from flask_restx import Namespace
from flask import Blueprint

# Private Imports
from views.offline_view import CheckText
from api import api

blueprint = Blueprint('api', __name__, url_prefix='/api')
api.init_app(blueprint)

offline_namespace = Namespace('Offline')
offline_namespace.add_resource(CheckText, '/check_text')

api.add_namespace(offline_namespace)
