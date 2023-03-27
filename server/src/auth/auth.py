from datetime import datetime, timedelta
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import create_access_token
import shortuuid
from src.auth.service import create_password_hash

from src.auth.service import verify_user
from src.users.crud import get_user, set_user

auth_blueprint = Blueprint("auth", __name__)
api = Api(auth_blueprint)

login = api.model(
    "Login",
    {
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


class Login(Resource):
    @api.expect(login, validate=True)
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        # Verify username and password
        user = verify_user(email, password)

        if user:
            access_token = create_access_token(
                identity=email, expires_delta=timedelta(hours=2)
            )
            response_object["token"] = access_token
            return response_object, 200
        else:
            response_object["message"] = "Invalid credentials."
            return response_object, 401


class Register(Resource):
    @api.expect(login, validate=True)
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        user = {
            "id": shortuuid.uuid(),
            "password": create_password_hash(password),
            "email": email,
            "created_date": datetime.utcnow().isoformat(),
            "recipes": [],
        }
        set_user(email, user)

        response_object["message"] = f"{email} was added!"
        access_token = create_access_token(
            identity=email, expires_delta=timedelta(hours=2)
        )
        response_object["token"] = access_token
        return response_object, 201


api.add_resource(Login, "/auth/login")
api.add_resource(Register, "/auth/register")
