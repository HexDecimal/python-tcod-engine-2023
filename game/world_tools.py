from tcod.ecs import World

import game.tiles
from game.actor_tools import new_actor
from game.components import Context, Graphic, MapDict, Player, Position
from game.map_tools import TestMap, activate_map
from game.messages import MessageLog


def new_world() -> World:
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
    activate_map(world, TestMap())
    ctx.player = new_actor(world, (Position(1, 1), Graphic(ord("@")), Player()))
    return world
