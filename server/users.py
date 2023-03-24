from datetime import datetime
import shortuuid
from flask import Blueprint, request
from flask_restx import Resource, Api, fields
from db import redis_client

def get_user(email):
    user = redis_client.json().get(f"users:{email}")
    return user
    
def set_user(email, user_obj):
    redis_client.json().set(f"users:{email}", '$', user_obj)
    return user_obj


users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
    'chats': fields.List(fields.String)
})

class UsersList(Resource):

    @api.expect(user, validate=True)
    def post(self):
        post_data = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')
        response_object = {}

        user = get_user(email)
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400
        
        user = {
            "id": shortuuid.uuid(),
            "username": username,
            "email": email,
            "created_date": datetime.now(),
            "chats": []
        }
        set_user(email, user)

        response_object['message'] = f'{email} was added!'
        return response_object, 201
    
class Users(Resource):
    
    @api.marshal_with(user)
    def get(self, email):
        user = get_user(email)
        if not user:
            api.abort(404, f"User {email} does not exist")
        return user, 200


api.add_resource(UsersList, '/users')
api.add_resource(Users, '/users/<email>')