import os
from datetime import timedelta
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
SECRET_KEY=os.environ['SECRET_KEY']