"""
Advanced physics utilities for the InfoPhyzx organ.

Includes:
- Graph Laplacian (combinatorial + normalized)
- Diffusion operator
- Heat equation update
- Wave equation update
- Gradient + Divergence
- Vector-field update
- Full propagation engine
"""

from typing import Dict, List, Tuple
import math


# ---------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------

def zero_state(nodes: List[str]) -> Dict[str, float]:
    return {node: 0.0 for node in nodes}


def neighbors(node: str, edges: List[Tuple[str, str]]) -> List[str]:
    n = []
    for a, b in edges:
        if a == node:
            n.append(b)
        elif b == node:
            n.append(a)
    return n


def normalize(value: float) -> float:
    return max(min(value, 1.0), -1.0)


# ---------------------------------------------------------
# Degree + adjacency helpers
# ---------------------------------------------------------

def degree(node: str, edges: List[Tuple[str, str]]) -> int:
    return len(neighbors(node, edges))


def adjacency(node: str, edges: List[Tuple[str, str]]) -> List[str]:
    return neighbors(node, edges)


# ---------------------------------------------------------
# Graph Laplacian (combinatorial)
# ---------------------------------------------------------

def laplacian(state: Dict[str, float], edges: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    Lφ(i) = Σ_j (φ(j) - φ(i))
    """
    L = {}
    for node in state:
        nbrs = neighbors(node, edges)
        if not nbrs:
            L[node] = 0.0
            continue

        L[node] = sum(state[j] - state[node] for j in nbrs)
    return L


# ---------------------------------------------------------
# Normalized Laplacian
# ---------------------------------------------------------

def normalized_laplacian(state: Dict[str, float], edges: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    L_norm φ(i) = Σ_j (φ(j)/sqrt(d_i d_j)) - φ(i)
    """
    L = {}
    for node in state:
        d_i = degree(node, edges)
        if d_i == 0:
            L[node] = 0.0
            continue

        acc = 0.0
        for j in neighbors(node, edges):
            d_j = degree(j, edges)
            acc += state[j] / math.sqrt(d_i * d_j)

        L[node] = acc - state[node]
    return L


# ---------------------------------------------------------
# Diffusion operator (Heat equation)
# ---------------------------------------------------------

def diffuse(state: Dict[str, float], edges: List[Tuple[str, str]], D: float, dt: float) -> Dict[str, float]:
    """
    φ(t+dt) = φ(t) + dt * D * Laplacian(φ)
    """
    L = laplacian(state, edges)
    new_state = {}

    for node in state:
        new_state[node] = normalize(state[node] + dt * D * L[node])

    return new_state


# ---------------------------------------------------------
# Wave equation operator
# ---------------------------------------------------------

def wave_step(
    state: Dict[str, float],
    prev_state: Dict[str, float],
    edges: List[Tuple[str, str]],
    c: float,
    dt: float
) -> Dict[str, float]:
    """
    Discrete wave equation:
        φ(t+dt) = 2φ(t) - φ(t-dt) + c^2 * dt^2 * Laplacian(φ)
    """
    L = laplacian(state, edges)
    new_state = {}

    for node in state:
        new_state[node] = (
            2 * state[node]
            - prev_state[node]
            + (c * c) * (dt * dt) * L[node]
        )
        new_state[node] = normalize(new_state[node])

    return new_state


# ---------------------------------------------------------
# Gradient + Divergence (graph-based)
# ---------------------------------------------------------

def gradient(state: Dict[str, float], edges: List[Tuple[str, str]]) -> Dict[Tuple[str, str], float]:
    """
    Gradient on edges:
        grad(i,j) = φ(j) - φ(i)
    """
    G = {}
    for (i, j) in edges:
        G[(i, j)] = state[j] - state[i]
    return G


def divergence(grad: Dict[Tuple[str, str], float], nodes: List[str]) -> Dict[str, float]:
    """
    Divergence at nodes:
        div(i) = Σ_j grad(i,j)
    """
    div = {node: 0.0 for node in nodes}

    for (i, j), val in grad.items():
        div[i] -= val
        div[j] += val

    return div


# ---------------------------------------------------------
# Vector-field influence update
# ---------------------------------------------------------

def vector_update(state: Dict[str, float], edges: List[Tuple[str, str]], influence: float) -> Dict[str, float]:
    new_state = {}

    for node in state:
        nbrs = neighbors(node, edges)
        if not nbrs:
            new_state[node] = state[node]
            continue

        avg_nbr = sum(state[j] for j in nbrs) / len(nbrs)
        new_state[node] = normalize(state[node] + influence * avg_nbr)

    return new_state


# ---------------------------------------------------------
# Full propagation engine
# ---------------------------------------------------------

def propagate_step(
    state: Dict[str, float],
    edges: List[Tuple[str, str]],
    dt: float,
    D: float = 0.1,
    influence: float = 0.05,
    use_normalized_laplacian: bool = False
) -> Dict[str, float]:
    """
    Combined propagation:
    - Diffusion (heat equation)
    - Optional normalized Laplacian
    - Vector-field influence
    """

    # 1. Choose Laplacian
    if use_normalized_laplacian:
        L = normalized_laplacian(state, edges)
        diffused = {n: normalize(state[n] + dt * D * L[n]) for n in state}
    else:
        diffused = diffuse(state, edges, D=D, dt=dt)

    # 2. Vector influence
    updated = vector_update(diffused, edges, influence=influence)

    return updated
