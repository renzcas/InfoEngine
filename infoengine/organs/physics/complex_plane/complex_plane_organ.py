from .panel import Panel
from .tracker import Tracker
from .colors import ColorMap


class ComplexPlaneOrgan:
    def __init__(self):
        self.panel = Panel()
        self.tracker = Tracker()
        self.colors = ColorMap()

    def generate_field(self):
        return {
            "panel": self.panel.describe(),
            "tracker": self.tracker.state(),
            "colors": self.colors.scheme(),
        }
