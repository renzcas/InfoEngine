from pydantic import BaseModel
from typing import List, Tuple, Optional


# ---------------------------------------------------------
# Field initialization
# ---------------------------------------------------------

class FieldRequest(BaseModel):
    """
    Initialize a field with:
    - nodes: list of node names
    - edges: list of (nodeA, nodeB) pairs
    """
    nodes: List[str]
    edges: List[Tuple[str, str]]


# ---------------------------------------------------------
# Basic step request
# ---------------------------------------------------------

class StepRequest(BaseModel):
    """
    Basic propagation step:
    - dt: timestep
    - D: diffusion coefficient
    - influence: vector-field influence
    - mode: which operator to use
    """
    dt: float = 0.1
    D: float = 0.1
    influence: float = 0.05
    mode: str = "propagate"  # options: propagate, diffuse, wave, laplacian


# ---------------------------------------------------------
# Wave equation step
# ---------------------------------------------------------

class WaveStepRequest(BaseModel):
    """
    Wave equation update:
    - dt: timestep
    - c: wave speed
    """
    dt: float = 0.1
    c: float = 1.0


# ---------------------------------------------------------
# Direct Laplacian request
# ---------------------------------------------------------

class LaplacianRequest(BaseModel):
    """
    Compute Laplacian or normalized Laplacian.
    """
    normalized: bool = False


# ---------------------------------------------------------
# Full propagation request
# ---------------------------------------------------------

class PropagationRequest(BaseModel):
    """
    Full physics propagation:
    - dt: timestep
    - D: diffusion coefficient
    - influence: vector-field influence
    - use_normalized_laplacian: toggle
    """
    dt: float = 0.1
    D: float = 0.1
    influence: float = 0.05
    use_normalized_laplacian: bool = False
