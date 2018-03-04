from flask import Blueprint

personal = Blueprint('personal', __name__)

from .personal import *