from flask import Flask
from users import users_blueprint
from chats import chats_blueprint

app = Flask(__name__)

app.register_blueprint(users_blueprint)
app.register_blueprint(chats_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)