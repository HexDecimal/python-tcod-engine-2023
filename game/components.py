import attrs
from attrs import Factory, field

from game.entity import Entity
from game.sched import TurnQueue


@attrs.define
class Context:
    active_map: Entity = field(init=False)
    player: Entity = field(init=False)
    sched: TurnQueue[Entity] = Factory(TurnQueue)
    actors: set[Entity] = Factory(set)


@attrs.define
class Position:
    x: int = 0
    y: int = 0

    def set(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


@attrs.define
class Graphic:
    ch: int = ord("?")
    fg: tuple[int, int, int] = (255, 255, 255)


@attrs.define
class Player:
    pass
