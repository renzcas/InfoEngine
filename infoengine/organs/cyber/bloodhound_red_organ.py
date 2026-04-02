class BloodhoundRedOrgan:
    def __init__(self):
        self._state = {"status": "red online"}

    def state(self):
        return self._state

    def compute(self):
        pass
