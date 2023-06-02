"""Tools for working with the world."""
from tcod.ecs import World

import game.tiles
from game.components import Context, MapDict, Position
from game.map import MapKey
from game.map_tools import activate_map
from game.mapgen.test import test_map
from game.messages import MessageLog
from game.monsters import spawn
from game.tags import IsPlayer


def new_world() -> World:
    """Return a newly generated World."""
    world = World()
    world.global_.components.update(
        {
            Context: Context(),
            MapDict: MapDict(),
            MessageLog: MessageLog(),
        }
    )
    game.tiles.init(world)
    ctx = world.global_.components[Context]
    activate_map(world, MapKey(test_map))
    ctx.player = spawn("player", ctx.active_map, Position(1, 1))
    ctx.player.tags.add(IsPlayer)
    return world
