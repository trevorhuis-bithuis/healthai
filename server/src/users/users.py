from datetime import datetime
import shortuuid
from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src.users.crud import get_user, set_user, delete_user

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.String(readOnly=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
        "recipes": fields.List(fields.String),
    },
)


class UsersList(Resource):
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        email = post_data.get("email")
        response_object = {}

        user = get_user(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400

        user = {
            "id": shortuuid.uuid(),
            "email": email,
            "created_date": datetime.utcnow().isoformat(),
            "recipes": [],
        }
        set_user(email, user)

        response_object["message"] = f"{email} was added!"
        return response_object, 201


class Users(Resource):
    @api.marshal_with(user)
    def get(self, email):
        user = get_user(email)
        if not user:
            api.abort(404, f"User {email} does not exist")
        return user, 200

    @api.marshal_with(user)
    def delete(self, email):
        user = get_user(email)
        if not user:
            api.abort(404, f"User {email} does not exist")
        delete_user(email)
        return user, 200


api.add_resource(UsersList, "/users")
api.add_resource(Users, "/users/<email>")
