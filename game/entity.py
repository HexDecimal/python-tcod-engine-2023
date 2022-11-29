from typing import Optional, Type, TypeVar

T = TypeVar("T")


class Entity:
    def __init__(self, *components: T):
        self._components = dict[Type[T], T]()
        for c in components:
            self.add(c)

    def add(self, component: T) -> None:
        """Add a component to this entity."""
        assert component.__class__ not in self._components
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

    def __repr__(self) -> str:
        items = ", ".join(repr(c) for c in self._components.values())
        return f"Entity({items})"
