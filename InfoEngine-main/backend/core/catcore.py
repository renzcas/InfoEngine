# backend/core/catcore.py

from typing import Any, Callable, Dict, Tuple, List

class Morphism:
    def __init__(self, name: str, dom: str, cod: str, func: Callable[[Any], Any]):
        self.name = name
        self.dom = dom
        self.cod = cod
        self.func = func

    def __call__(self, x: Any) -> Any:
        return self.func(x)

    def __repr__(self) -> str:
        return f"{self.name}: {self.dom} -> {self.cod}"


class Category:
    def __init__(self, name: str):
        self.name = name
        self.objects: List[str] = []
        self.morphisms: Dict[Tuple[str, str, str], Morphism] = {}

    def add_object(self, obj: str):
        if obj not in self.objects:
            self.objects.append(obj)

    def add_morphism(self, m: Morphism):
        key = (m.name, m.dom, m.cod)
        self.add_object(m.dom)
        self.add_object(m.cod)
        self.morphisms[key] = m

    def compose(self, g: Morphism, f: Morphism) -> Morphism:
        if f.cod != g.dom:
            raise ValueError("Cannot compose: cod(f) != dom(g)")

        def h(x: Any) -> Any:
            return g(f(x))

        name = f"{g.name}∘{f.name}"
        return Morphism(name, f.dom, g.cod, h)

    def __repr__(self) -> str:
        return f"Category({self.name}, objects={self.objects}, morphisms={list(self.morphisms.keys())})"


class Functor:
    def __init__(self, name: str, source: Category, target: Category):
        self.name = name
        self.source = source
        self.target = target
        self.object_map: Dict[str, str] = {}
        self.morphism_map: Dict[Tuple[str, str, str], Morphism] = {}

    def map_object(self, a: str, fa: str):
        self.object_map[a] = fa
        self.target.add_object(fa)

    def map_morphism(self, m: Morphism, fm: Morphism):
        key_src = (m.name, m.dom, m.cod)
        self.morphism_map[key_src] = fm
        self.target.add_morphism(fm)

    def F_obj(self, a: str) -> str:
        return self.object_map[a]

    def F_mor(self, m: Morphism) -> Morphism:
        key_src = (m.name, m.dom, m.cod)
        return self.morphism_map[key_src]

    def __repr__(self) -> str:
        return f"Functor({self.name}: {self.source.name} -> {self.target.name})"
