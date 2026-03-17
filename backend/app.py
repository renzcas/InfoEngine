import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({"status": "alive", "organism": "InfoEngine"})

    # InfoPhyzx
    try:
        from organs.infophyzx import infophyzx_bp
        app.register_blueprint(infophyzx_bp, url_prefix="/infophyzx")
    except Exception:
        pass

    # CyberArena
    try:
        from organs.cyberarena import cyberarena_bp
        app.register_blueprint(cyberarena_bp, url_prefix="/cyber")
    except Exception:
        pass

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
