# wigner_compression.py

import torch

def wigner_curvature_penalty(W: torch.Tensor, x: torch.Tensor, p: torch.Tensor, lam: float = 1e-3):
    """
    W: [Nx, Np] Wigner function
    x: [Nx] position grid
    p: [Np] momentum grid
    lam: strength of compression penalty

    returns: scalar penalty
    """
    dx = x[1] - x[0]
    dp = p[1] - p[0]

    # finite differences for gradients
    dW_dx = (W[2:, 1:-1] - W[:-2, 1:-1]) / (2 * dx)
    dW_dp = (W[1:-1, 2:] - W[1:-1, :-2]) / (2 * dp)

    # curvature magnitude ~ gradient energy
    grad_sq = dW_dx[:, 1:-1]**2 + dW_dp[1:-1, :]**2
    penalty = lam * grad_sq.mean()
    return penalty
