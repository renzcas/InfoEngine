# organs/complex_plane/colors.py
from typing import Tuple
from .tracker import ComplexPlaneTracker

def divergence_to_color(rate: float) -> Tuple[int, int, int]:
    # simple mapping: blue (stable) → red (divergent)
    if rate < -0.5:
        return (0, 0, 255)      # strong convergence
    if rate < 0.1:
        return (0, 128, 255)    # mild convergence / stable
    if rate < 0.5:
        return (0, 255, 0)      # neutral / orbiting
    if rate < 1.5:
        return (255, 165, 0)    # unstable
    return (255, 0, 0)          # chaotic

def colorized_summary(tracker: ComplexPlaneTracker):
    items = tracker.summary()
    for item in items:
        rate = item["divergence_rate"]
        item["color_rgb"] = divergence_to_color(rate)
    return items
