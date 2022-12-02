import reprlib
from typing import Optional, Type, TypeVar

T = TypeVar("T")


class Entity:
    __slots__ = ("_components", "__weakref__")

    def __init__(self, *components: T):
        self._components = dict[Type[T], T]()
        self.set(*components)

    def add(self, *components: T) -> None:
        """Add components to this entity."""
        for component in components:
            assert component.__class__ not in self._components
            self._components[component.__class__] = component

    def set(self, *components: T) -> None:
        """Assign or replace the components of this entity."""
        for component in components:
            self._components[component.__class__] = component

    def get(self, kind: Type[T]) -> Optional[T]:
        """Return a component, or None if it doesn't exist."""
        return self._components.get(kind)

    def __getitem__(self, key: Type[T]) -> T:
        """Return a component of type, raises KeyError if it doesn't exist."""
        return self._components[key]

    def __setitem__(self, key: Type[T], value: T) -> None:
        """Set or replace a component."""
        self._components[key] = value

    def __delitem__(self, key: Type[T]) -> None:
        """Delete a component."""
        del self._components[key]

    def __contains__(self, key: Type[T]) -> bool:
        """Return true if a type of component exists in this entity."""
        return key in self._components

    @reprlib.recursive_repr()
    def __repr__(self) -> str:
        return f"""Entity({", ".join(repr(component) for component in self._components.values())})"""
