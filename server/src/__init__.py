from flask import Flask, jsonify
from flask_restx import Api, Resource

app = Flask(__name__)

api = Api(app)

app.config.from_object('src.config.DevelopmentConfig')

class Ping(Resource):
    def get(self):
        return {
            'status': 'success',
            'message': 'pong!'
        }
        
api.add_resource(Ping, '/ping');