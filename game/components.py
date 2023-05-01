"""Definitions of common component types."""
from __future__ import annotations

from typing import Self

import attrs
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
    def xy(self) -> tuple[int, int]:
        return self.x, self.y

    @property
    def yx(self) -> tuple[int, int]:
        return self.y, self.x


@attrs.define(frozen=True)
class Direction(Position):
    pass


@attrs.define(frozen=True)
class Graphic:
    ch: int = ord("?")
    fg: tuple[int, int, int] = (255, 255, 255)


@attrs.define(frozen=True)
class Player:
    pass


@attrs.define(frozen=True, kw_only=True)
class Stairway:
    down: MapKey | None = None
    up: MapKey | None = None


class MapDict(dict[MapKey, Entity]):
    pass
