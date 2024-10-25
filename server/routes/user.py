from flask import Blueprint
from ..controllers.user import login, signup

user = Blueprint("user", __name__)

user.add_url_rule("/login", view_func=login, methods=['POST'])
user.add_url_rule("/signup", view_func=signup, methods=['POST'])