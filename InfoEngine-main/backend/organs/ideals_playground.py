from flask import Blueprint, request, jsonify

ideals_bp = Blueprint("ideals_playground", __name__)

def compute_ideals_mod_n(n):
    ideals = []
    for k in range(n):
        if (n % k == 0) if k != 0 else False:
            ideals.append({
                "generator": k,
                "elements": [(k * i) % n for i in range(n)]
            })
    return ideals

@ideals_bp.route("/ideals", methods=["POST"])
def ideals():
    data = request.get_json()
    n = int(data["n"])
    return jsonify({"ideals": compute_ideals_mod_n(n)})
