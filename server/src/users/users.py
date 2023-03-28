from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Api, Resource, fields

from src.users.crud import get_user, delete_user
from src.diet.crud import get_user_recipes
from src.exercise.crud import get_user_workouts
from src.diet.diet import recipe
from src.exercise.exercise import workout

users_blueprint = Blueprint("users", __name__)
api = Api(users_blueprint)

user = api.model(
    "User",
    {
        "id": fields.String(readOnly=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True, writeOnly=True),
        "created_date": fields.DateTime,
        "recipes": fields.List(fields.Nested(recipe)),
        "workouts": fields.List(fields.Nested(workout)),
    },
)


class Users(Resource):
    @api.marshal_with(user)
    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user = get_user(email)
        if not user:
            api.abort(404, f"User {email} does not exist")
        response_object = {}

        recipes = get_user_recipes(user["recipes"])
        workouts = get_user_workouts(user["workouts"])
        response_object["id"] = user["id"]
        response_object["email"] = user["email"]
        response_object["created_date"] = user["created_date"]
        response_object["recipes"] = recipes
        response_object["workouts"] = workouts
        return response_object, 200

    @api.marshal_with(user)
    @jwt_required()
    def delete(self):
        email = get_jwt_identity()
        user = get_user(email)
        if not user:
            api.abort(404, f"User {email} does not exist")
        delete_user(email)
        return user, 200


api.add_resource(Users, "/user")
