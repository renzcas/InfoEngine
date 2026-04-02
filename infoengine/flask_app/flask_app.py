from flask import Flask

# Create the Flask application
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "Flask side of InfoEngine is online."
