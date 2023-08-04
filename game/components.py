"""Definitions of common component types."""
from __future__ import annotations

from typing import Self

import attrs
import tcod.ecs.callbacks
from attrs import Factory, field
from tcod.ecs import Entity

from game.map import MapKey
from game.sched import TurnQueue


@attrs.define()
class Context:
    active_map: Entity = field(init=False)
    player: Entity = field(init=False)
    sched: TurnQueue[Entity] = Factory(TurnQueue)


@attrs.define(frozen=True)
class Position:
    """The 2D position of an entity."""

    x: int = 0
    y: int = 0

    def __add__(self, other: Position | tuple[int, int]) -> Self:
        if isinstance(other, tuple):
            return self.__class__(x=self.x + other[0], y=self.y + other[1])
        if isinstance(other, Position):
            return self.__class__(x=self.x + other.x, y=self.y + other.y)
        return NotImplemented

    def __sub__(self, other: Position | tuple[int, int]) -> Self:
        if isinstance(other, tuple):
            return self.__class__(x=self.x - other[0], y=self.y - other[1])
        if isinstance(other, Position):
            return self.__class__(x=self.x - other.x, y=self.y - other.y)
        return NotImplemented

    @property
    def chebyshev_normalize(self) -> Self:
        """Normalize this vector to a single step in Chebyshev distance."""
        return self.__class__(
            0 if self.x == 0 else -1 if self.x < 0 else 1,
            0 if self.y == 0 else -1 if self.y < 0 else 1,
        )

    @property
    def xy(self) -> tuple[int, int]:
        """Return an (x, y) tuple."""
        return self.x, self.y

    @property
    def yx(self) -> tuple[int, int]:
        """Return an (i, j) tuple, for Numpy indexing."""
        return self.y, self.x


@tcod.ecs.callbacks.register_component_changed(component=Position)
def on_position_changed(entity: Entity, old: Position | None, new: Position | None) -> None:
    """Replicate Position component values as tags."""
    if old == new:
        return
    if old is not None:
        entity.tags.remove(old)
    if new is not None:
        entity.tags.add(new)


@attrs.define(frozen=True)
class Direction(Position):
    pass


@attrs.define(frozen=True)
class Graphic:
    """A simple entity graphic."""

    ch: int = ord("?")
    fg: tuple[int, int, int] = (255, 255, 255)


@attrs.define(frozen=True, kw_only=True)
class Stairway:
    down: MapKey | None = None
    up: MapKey | None = None


class MapDict(dict[MapKey, Entity]):
    pass
