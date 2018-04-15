from flask import Blueprint

circles = Blueprint('circles', __name__)

from .circles import *