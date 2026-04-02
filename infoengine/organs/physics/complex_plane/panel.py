# organs/complex_plane/panel.py
from typing import Dict, Any
from .tracker import tracker
from .colors import colorized_summary

def get_complex_plane_panel() -> Dict[str, Any]:
    trajectories = tracker.get_trajectories()
    loops = colorized_summary(tracker)
    return {
        "loops": loops,
        "trajectories": {
            name: [{"re": z.real, "im": z.imag} for z in traj]
            for name, traj in trajectories.items()
        },
    }
