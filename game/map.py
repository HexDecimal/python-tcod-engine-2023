"""Defines the Map class."""
from collections.abc import Callable, Hashable
from typing import Any, TypeVar

import attrs
import numpy as np
from numpy.typing import DTypeLike, NDArray
from tcod.ecs import Entity, World

T = TypeVar("T")


class MapAttribute:
    """A generic map attribute used as a key for generic maps."""

    def __init__(self, key: Hashable | None, dtype: DTypeLike, default: Any = 0) -> None:
        self.key = key if key is not None else self
        self.dtype = np.dtype(dtype)
        self.default = default


class Map:
    """A generic map array container.

    >>> map = Map(10, 10)
    >>> tiles = MapAttribute("tiles", np.uint8)  # Define new attribute.
    >>> tiles in map
    False
    >>> map[tiles][:] = 1
    >>> tiles in map
    True
    >>> map[tiles].shape
    (10, 10)
    >>> map[tiles][0, 0]
    1
    >>> monster = {"my_explored_attr": MapAttribute(None, np.bool8)}  # Define anonymous attribute.
    >>> map[monster["my_explored_attr"]][:] = 0
    """

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self._data: dict[Hashable, NDArray[Any]] = {}

    def __contains__(self, attr: MapAttribute) -> bool:
        if attr.key not in self._data:
            return False
        assert self._data[attr.key].dtype == attr.dtype
        return True

    def __getitem__(self, attr: MapAttribute) -> NDArray[Any]:
        if attr.key not in self._data:
            self._data[attr.key] = np.full((self.height, self.width), fill_value=attr.default, dtype=attr.dtype)
        array = self._data[attr.key]
        assert array.dtype == attr.dtype
        return array

    def __setitem__(self, attr: MapAttribute, array: NDArray[Any]) -> None:
        assert attr.dtype == array.dtype, "Consider adding [:] for full array assignment."
        self._data[attr.key] = array

    def __delitem__(self, attr: MapAttribute) -> None:
        del self._data[attr.key]


@attrs.define(frozen=True)
class MapKey:
    """An immutable key used to lazily reference a map."""

    def generate(self, world: World) -> Entity:
        """Generate this map with its own parameters."""
        raise NotImplementedError()


@attrs.define(frozen=True)
class UniqueMapKey(MapKey):
    generator: Callable[[World], Entity]

    def generate(self, world: World) -> Entity:
        return self.generator(world)
