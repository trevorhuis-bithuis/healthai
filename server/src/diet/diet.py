from datetime import datetime
import shortuuid
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.diet.openai import generate_recipe
from src.diet.crud import get_recipe, set_recipe, add_recipe_to_user

diet_blueprint = Blueprint("diet", __name__)
api = Api(diet_blueprint)

recipe_generate = api.model(
    "RecipeGenerate",
    {
        "ingredients": fields.List(fields.String),
        "allergies": fields.List(fields.String),
    },
)

recipe = api.model(
    "Recipe",
    {
        "id": fields.String(readOnly=True),
        "user_email": fields.String(),
        "title": fields.String(),
        "ingredients": fields.List(fields.String),
        "instructions": fields.List(fields.String),
        "created_date": fields.DateTime(readOnly=True),
    },
)


class RecipesList(Resource):
    @api.expect(recipe, validate=True)
    def post(self):
        post_data = request.get_json()
        current_user = get_jwt_identity()
        email = current_user["email"]
        recipe = post_data.get("recipe")
        response_object = {}

        recipe = {
            "id": shortuuid.uuid(),
            "user_email": email,
            "title": recipe.get("title"),
            "ingredients": recipe.get("ingredients"),
            "instructions": recipe.get("instructions"),
            "created_date": datetime.utcnow().isoformat(),
        }

        set_recipe(recipe)
        add_recipe_to_user(email, recipe["id"])

        response_object["recipe"] = recipe
        response_object["message"] = "Recipe created!"
        return response_object, 201


class RecipesGenerate(Resource):
    @api.expect(recipe_generate, validate=True)
    @jwt_required()
    def post(self):
        post_data = request.get_json()
        ingredients = post_data.get("ingredients")
        allergies = post_data.get("allergies")
        response_object = {}

        recipe = generate_recipe(ingredients, allergies)

        response_object["message"] = "Recipe generated!"
        response_object["recipe"] = recipe
        return response_object, 201


class Recipes(Resource):
    @api.marshal_with(recipe)
    def get(self, id):
        return get_recipe(id), 200


api.add_resource(RecipesList, "/diet/recipes")
api.add_resource(RecipesGenerate, "/diet/recipes/generate")
api.add_resource(Recipes, "/diet/recipes/<id>")
