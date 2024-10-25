from flask import request
from flask_jwt_extended import create_access_token
from ..utils.serverUtils import bcrypt
from ..db.connection import db
from ..utils.response import APIResponse, APIError

def login():
    body = request.get_json()
    user = db.users.find_one({"email": body["email"],})
    if user and "password" in user:
        if bcrypt.check_password_hash(user["password"], body["password"]):
            token = create_access_token(identity=body["email"])
            return APIResponse(200, {
                "name": user["name"],
                "email": user["email"],
                "token": token
            }).json
        return APIError(200, "Password incorrect").json
    return APIError(200, "Email id not registered").json

def signup():
    body = request.get_json()
    existUser = db.users.find_one({"email": body["email"]})
    
    if not existUser:
        hashedPassword = bcrypt.generate_password_hash(body["password"]).decode()
        user = {
            "name": user['name'],
            "email": user['email'],
            "password": hashedPassword
        }
        db.users.insert_one(user)

        return APIResponse(200, None).json
    return APIError(200, "Email id already exists").json