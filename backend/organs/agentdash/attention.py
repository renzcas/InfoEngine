from collections import defaultdict
from math import exp

class AttentionTensor:
    def __init__(self):
        self.tensor = defaultdict(lambda: defaultdict(float))

    def bump(self, kind: str, source: str, amount: float):
        self.tensor[kind][source] += amount

    def decay(self, rate: float = 0.01):
        for kind in self.tensor:
            for source in self.tensor[kind]:
                self.tensor[kind][source] *= (1 - rate)

    def export(self):
        return self.tensor

attention_tensor = AttentionTensor()
