import numpy as np
from flask import Blueprint, request, jsonify

matrix_bp = Blueprint("matrix_playground", __name__)

@matrix_bp.route("/eigen", methods=["POST"])
def matrix_eigen():
    data = request.get_json()

    # Expect: { "matrix": [[a, b], [c, d]] }
    matrix = np.array(data["matrix"], dtype=float)

    vals, vecs = np.linalg.eig(matrix)

    return jsonify({
        "eigenvalues": vals.tolist(),
        "eigenvectors": vecs.tolist()
    })
