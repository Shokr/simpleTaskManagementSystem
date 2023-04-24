from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .tasks import *
