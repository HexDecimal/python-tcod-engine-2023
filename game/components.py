from __future__ import annotations

from typing import Self

import attrs
from attrs import Factory, field
from tcod.ec import ComponentDict

from game.sched import TurnQueue


@attrs.define()
class Context:
    active_map: ComponentDict = field(init=False)
    player: ComponentDict = field(init=False)
    sched: TurnQueue[ComponentDict] = Factory(TurnQueue)
    actors: set[ComponentDict] = Factory(set)


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


@attrs.define(frozen=True)
class Stairway:
    destination: tuple[str, int]


@attrs.define()
class MapFeatures:
    features: list[ComponentDict] = Factory(list)
