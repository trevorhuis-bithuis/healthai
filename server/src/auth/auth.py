from datetime import timedelta
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import create_access_token

from src.auth.service import verify_user

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
            response_object["access_token"] = access_token
            return response_object, 200
        else:
            response_object["message"] = "Invalid credentials."
            return response_object, 401


api.add_resource(Login, "/auth/login")
