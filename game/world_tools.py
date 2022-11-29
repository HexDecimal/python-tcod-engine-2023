from game.components import Context, Position
from game.entity import Entity


def new_world() -> Entity:
    world = Entity(Context())
    ctx = world[Context]
    ctx.player = Entity(Position(0, 0))
    return world
