from tcod.ec import ComponentDict

from game.actor_tools import new_actor
from game.components import Context, Graphic, Player, Position
from game.map_tools import new_map


def new_world() -> ComponentDict:
    world = ComponentDict([Context()])
    ctx = world[Context]
    ctx.active_map = new_map(50, 50)
    ctx.player = new_actor(world, (Position(1, 1), Graphic(ord("@")), Player()))
    return world
