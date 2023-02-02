import attrs
from attrs import Factory, field
from tcod.ec import ComponentDict

from game.sched import TurnQueue


@attrs.define
class Context:
    active_map: ComponentDict = field(init=False)
    player: ComponentDict = field(init=False)
    sched: TurnQueue[ComponentDict] = Factory(TurnQueue)
    actors: set[ComponentDict] = Factory(set)


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
