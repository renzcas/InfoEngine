import numpy as np
from typing import Dict, Any, Tuple, List


class GeometryOrgan:
    def __init__(self, grid_size: Tuple[int, int] = (32, 32)):
        self.w, self.h = grid_size
        self.grid_size = grid_size
        self.phase = 0.0

    def step(self, dt: float, t: float) -> Dict[str, Any]:
        self.phase += dt

        x = np.linspace(-1, 1, self.w)
        y = np.linspace(-1, 1, self.h)
        X, Y = np.meshgrid(x, y)

        r = np.sqrt(X**2 + Y**2)
        curvature = np.sin(3 * r - self.phase) * np.exp(-2 * r**2)

        curvature_field = curvature.flatten().tolist()

        attractors = [
            {"id": "A1", "x": 0.25, "y": 0.7, "strength": 1.2},
            {"id": "A2", "x": 0.75, "y": 0.3, "strength": 0.9},
        ]

        gy, gx = np.gradient(curvature)
        flow_vectors: List[Dict[str, float]] = []
        for i in range(self.h):
            for j in range(self.w):
                if (i % 4 == 0) and (j % 4 == 0):
                    flow_vectors.append(
                        {
                            "x": j / (self.w - 1),
                            "y": i / (self.h - 1),
                            "vx": float(-gx[i, j]),
                            "vy": float(-gy[i, j]),
                        }
                    )

        complexity = float(np.mean(np.abs(curvature)))

        return {
            "grid_size": [self.w, self.h],
            "curvature_field": curvature_field,
            "attractors": attractors,
            "flow_vectors": flow_vectors,
            "complexity": complexity,
        }
