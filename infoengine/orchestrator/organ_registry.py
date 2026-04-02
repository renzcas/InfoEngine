from .import_map import IMPORT_MAP

class OrganRegistry:
    def __init__(self):
        self.organs = {}
        self._auto_register()

    def _auto_register(self):
        for name, cls in IMPORT_MAP.items():
            try:
                self.organs[name] = cls()
            except Exception as e:
                self.organs[name] = {"error": str(e)}

    def get(self, name: str):
        return self.organs.get(name)

    def all(self):
        return list(self.organs.keys())
