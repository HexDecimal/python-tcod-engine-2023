from game.components import Context, Position
from game.entity import Entity
from game.map_tools import new_map


def new_world() -> Entity:
    world = Entity(Context())
    ctx = world[Context]
    ctx.player = Entity(Position(1, 1))
    ctx.active_map = new_map(50, 50)
    return world
