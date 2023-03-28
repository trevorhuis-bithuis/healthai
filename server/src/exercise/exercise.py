from datetime import datetime
import shortuuid
from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.exercise.openai import generate_workout
from src.exercise.crud import get_workout, set_workout, add_workout_to_user

exercise_blueprint = Blueprint("exercise", __name__)
api = Api(exercise_blueprint)

workout_generate = api.model(
    "WorkoutGenerate",
    {
        "duration": fields.Integer(required=True),
        "muscles": fields.List(fields.String, required=True),
    },
)

workout = api.model(
    "Workout",
    {
        "id": fields.String(readOnly=True),
        "user_email": fields.String(),
        "title": fields.String(),
        "steps": fields.List(fields.String),
        "created_date": fields.DateTime(readOnly=True),
    },
)


class WorkoutsList(Resource):
    @api.expect(workout, validate=True)
    @jwt_required()
    def post(self):
        post_data = request.get_json()
        email = get_jwt_identity()
        steps = post_data.get("steps")
        title = post_data.get("title")
        response_object = {}

        workout = {
            "id": shortuuid.uuid(),
            "user_email": email,
            "title": title,
            "steps": steps,
            "created_date": datetime.utcnow().isoformat(),
        }

        set_workout(workout)
        add_workout_to_user(email, workout["id"])

        response_object["workout"] = workout
        response_object["message"] = "Workout created!"
        return response_object, 201


class WorkoutsGenerate(Resource):
    @api.expect(workout_generate, validate=True)
    @jwt_required()
    def post(self):
        post_data = request.get_json()
        muscles = post_data.get("muscles")
        duration = post_data.get("duration")
        response_object = {}

        title = f"{duration} minute {' '.join(muscles)} workout"
        workout = generate_workout(duration, muscles)

        response_object["message"] = "Workout generated!"
        response_object["workout"] = {"steps": workout, "title": title}
        return response_object, 201


class Workouts(Resource):
    @api.marshal_with(workout)
    def get(self, id):
        return get_workout(id), 200


api.add_resource(WorkoutsList, "/exercise/workouts")
api.add_resource(WorkoutsGenerate, "/exercise/workouts/generate")
api.add_resource(Workouts, "/exercise/workouts/<id>")
