from tcod.ec import ComponentDict

import game.tiles
from game.actor_tools import new_actor
from game.components import Context, Graphic, MapDict, Player, Position
from game.map_tools import TestMap, activate_map


def new_world() -> ComponentDict:
    world = ComponentDict([Context(), MapDict()])
    game.tiles.init(world)
    ctx = world[Context]
    activate_map(world, TestMap())
    ctx.player = new_actor(world, (Position(1, 1), Graphic(ord("@")), Player()))
    return world
