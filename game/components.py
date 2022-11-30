from game.entity import Entity


class Context:
    active_map: Entity
    player: Entity


class Position:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
