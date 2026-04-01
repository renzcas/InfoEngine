from flask import Flask

flask_app = Flask(__name__)

@flask_app.route("/flask-heartbeat")
def flask_beat():
    return {"status": "flask alive"}
