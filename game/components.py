import attrs

from game.entity import Entity
from game.sched import TurnQueue


@attrs.define
class Context:
    active_map: Entity
    player: Entity
    sched: TurnQueue[Entity]
    actors: list[Entity]

    def __init__(self) -> None:
        self.sched = TurnQueue()
        self.actors = []


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
