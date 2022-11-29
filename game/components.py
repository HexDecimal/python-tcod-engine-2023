import game.entity


class Context:
    active_map: game.entity.Entity
    player: game.entity.Entity


class Position:
    __slots__ = ("x", "y")

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
