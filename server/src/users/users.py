from flask import Blueprint
from flask_restx import Api, Resource, fields

from src.users.crud import get_user, delete_user

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.String(readOnly=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True, writeOnly=True),
        "created_date": fields.DateTime,
        "recipes": fields.List(fields.String),
    },
)


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


api.add_resource(Users, "/users/<email>")
