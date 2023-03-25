from datetime import datetime
import shortuuid
from flask import Blueprint, request
from flask_restx import Api, Resource, fields

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

recipe_input = api.model(
    "RecipeInput",
    {
        "recipe": fields.String(required=True),
        "user_email": fields.String(required=True),
    },
)

recipe_output = api.model(
    "RecipeOutput",
    {
        "id": fields.String,
        "recipe": fields.String,
        "created_date": fields.DateTime,
    },
)


class RecipesList(Resource):
    @api.expect(recipe_input, validate=True)
    def post(self):
        post_data = request.get_json()
        email = post_data.get("user_email")
        recipe = post_data.get("recipe")
        response_object = {}

        recipe = {
            "id": shortuuid.uuid(),
            "user_email": email,
            "recipe": recipe,
            "created_date": datetime.utcnow().isoformat(),
        }

        set_recipe(recipe)
        add_recipe_to_user(email, recipe["id"])

        response_object["recipe"] = recipe
        response_object["message"] = "Recipe created!"
        return response_object, 201


class RecipesGenerate(Resource):
    @api.expect(recipe_generate, validate=True)
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
    @api.marshal_with(recipe_output)
    def get(self, id):
        return get_recipe(id), 200


api.add_resource(RecipesList, "/diet/recipes")
api.add_resource(RecipesGenerate, "/diet/recipes/generate")
api.add_resource(Recipes, "/diet/recipes/<id>")
