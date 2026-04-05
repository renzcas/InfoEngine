# organs/wigner_organ.py

import torch
import torch.fft as fft

class WignerOrgan(torch.nn.Module):
    """
    Computes the Wigner function W(x,p) for a 1D wavefunction ψ(x)
    and provides negativity metrics (quantum-classical boundary gauge).
    """

    def __init__(self, hbar: float = 1.0):
        super().__init__()
        self.hbar = hbar

    def forward(self, psi_x: torch.Tensor, x: torch.Tensor, p: torch.Tensor):
        """
        psi_x: complex tensor [N]   -> wavefunction ψ(x)
        x:     real tensor   [N]   -> position grid
        p:     real tensor   [M]   -> momentum grid

        returns:
            W:     [N, M] real Wigner function
            stats: dict with negativity metrics
        """

        N = x.shape[0]
        dx = x[1] - x[0]

        # relative coordinate grid y
        y = x - x.mean()  # [N]

        # phase factor e^{2 i p y / ħ} → [M, N]
        phase = torch.exp(2j * torch.outer(p, y) / self.hbar)

        psi = psi_x
        psi_conj = psi.conj()

        W_rows = []
        for i in range(N):
            psi_plus  = torch.roll(psi,  i)     # ψ(x + y)
            psi_minus = torch.roll(psi_conj, -i)  # ψ*(x − y)
            corr = psi_plus * psi_minus         # [N]
            Wy = phase * corr                   # [M, N]
            W_rows.append((Wy * dx).sum(dim=-1).real)  # [M]

        W = torch.stack(W_rows, dim=0)  # [N, M]
        W = W / (torch.pi * self.hbar)

        # NEGATIVITY METER
        dp = p[1] - p[0]
        neg_mass = torch.clamp(-W, min=0).sum() * dx * dp
        total_mass = W.abs().sum() * dx * dp + 1e-12
        neg_ratio = neg_mass / total_mass

        stats = {
            "W_min": float(W.min()),
            "neg_mass": float(neg_mass),
            "neg_ratio": float(neg_ratio),
        }

        return W, stats
