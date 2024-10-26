from flask import Flask
from werkzeug.exceptions import HTTPException
from .routes.user import user
from .routes.whatsapp import whatsapp
from .utils.response import APIError

app = Flask(__name__)

app.config.from_pyfile("config.py")

app.register_blueprint(user)
app.register_blueprint(whatsapp)

@app.route("/")
def home():
    return "Hello World"
# @app.errorhandler(HTTPException)
# def httpExeptionHandler(error):
#     return APIError(error.code, error.description).json

# @app.errorhandler(Exception)
# def handleException(error):
#     return APIError(500, error.__doc__).json