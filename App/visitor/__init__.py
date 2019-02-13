from flask import Blueprint

bp = Blueprint('visitor', __name__)

from . import views
