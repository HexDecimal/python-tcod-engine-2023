from game.entity import Entity
from game.sched import TurnQueue


class Context:
    active_map: Entity
    player: Entity
    sched: TurnQueue[Entity]
    actors: list[Entity]

    def __init__(self) -> None:
        self.sched = TurnQueue()
        self.actors = []


class Position:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def set(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Graphic:
    __slots__ = ("ch", "fg")

    def __init__(self, ch: int = ord("?"), fg: tuple[int, int, int] = (255, 255, 255)) -> None:
        self.ch = ch
        self.fg = fg


class Player:
    __slots__ = ()
