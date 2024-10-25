from flask import Blueprint

user = Blueprint("user", __name__)

user.add_url_rule("/login", view_func=login, methods=['POST'])