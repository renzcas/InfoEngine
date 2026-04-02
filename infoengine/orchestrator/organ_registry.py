class OrganRegistry:
    def __init__(self):
        self.organs = {}

    def register(self, name: str, organ):
        self.organs[name] = organ

    def get(self, name: str):
        return self.organs.get(name)
