from typing import Iterable, Type, TypeVar

T = TypeVar("T")


class Entity:
    def __init__(self, components: Iterable[T]):
        self._components = dict[Type[T], T]()
        for c in components:
            self.add(c)

    def add(self, component: T) -> None:
        assert component.__class__ not in self._components
        self._components[component.__class__] = component

    def __getitem__(self, key: Type[T]) -> T:
        return self._components[key]

    def __setitem__(self, key: Type[T], value: T) -> None:
        self._components[key] = value

    def __delitem__(self, key: Type[T]) -> None:
        del self._components[key]

    def __contains__(self, key: Type[T]) -> bool:
        return key in self._components
