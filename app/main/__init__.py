from flask import Blueprint

main = Blueprint('main', __name__) #To add a prefix Blueprint('name', __name__, url_prefix='prefix')

from . import views #Need this line to register views