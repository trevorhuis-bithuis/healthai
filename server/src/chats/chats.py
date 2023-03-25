from datetime import datetime

import shortuuid
from flask import Blueprint, request
from flask_restx import Api, Resource, fields

from src.db import redis_client
from src.users.crud import get_user, set_user


def get_chats_by_email(email):
    chat = redis_client.scan(f"chats:{email}:*")
    return chat


def get_chat(email, id):
    chat = redis_client.json().get(f"chats:{email}:{id}")
    return chat


def set_chat_by_email(email, chat_obj):
    redis_client.json().set(f"chats:{email}:{chat_obj['id']}", "$", chat_obj)
    return chat_obj


def add_chat_to_user(email, chat_id):
    user = get_user(email)
    user["chats"].append(chat_id)
    set_user(email, user)


def add_message_to_chat(email, chat_id, message):
    chat = get_chats_by_email(email, chat_id)
    chat["messages"].append(message)
    set_chat_by_email(email, chat)


chats_blueprint = Blueprint("chats", __name__)
api = Api(chats_blueprint)

chat_message = api.model(
    "ChatMessage",
    {
        "user_email": fields.String(required=True),
        "chat_id": fields.String(required=True),
        "author": fields.String(required=True),
        "message": fields.String(required=True),
    },
)

chat = api.model(
    "Chat",
    {
        "id": fields.String(readOnly=True),
        "user_email": fields.String(required=True),
        "created_date": fields.DateTime,
        "messages": fields.Nested(chat_message, as_list=True),
    },
)


class Chats(Resource):
    @api.marshal_with(chat)
    def get(self, email, id):
        return get_chat(email, id), 200


class AddMessageToChat(Resource):
    @api.expect(chat_message, validate=True)
    def post(self):
        post_data = request.get_json()
        user_email = post_data.get("user_email")
        chat_id = post_data.get("chat_id")
        message = post_data.get("message")
        response_object = {}

        add_message_to_chat(user_email, chat_id, message)

        response_object["message"] = "Message added!"
        return response_object, 201


class ChatsList(Resource):
    @api.marshal_with(chat, as_list=True)
    def get(self, email):
        return get_chats_by_email(email), 200

    @api.expect(chat, validate=True)
    def post(self, email):
        post_data = request.get_json()
        messages = post_data.get("messages")
        response_object = {}

        set_chat_by_email(
            email,
            {
                "id": shortuuid.uuid(),
                "user_email": email,
                "created_date": datetime.utcnow().isoformat(),
                "messages": messages,
            },
        )

        add_chat_to_user(email, chat["id"])

        response_object["message"] = "Chat created!"
        return response_object, 201


api.add_resource(Chats, "/chats/<email>/<id>")
api.add_resource(AddMessageToChat, "/chats/add-message")
api.add_resource(ChatsList, "/chats/<email>")