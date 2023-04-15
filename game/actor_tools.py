import itertools
from collections.abc import Iterable

import numpy as np
import tcod
import tcod.map
from tcod.ec import ComponentDict

import game.map_attrs
from game.actor_types import ActiveFOV, Memory, MemoryLayer
from game.components import Context, Graphic, MapFeatures, Position
from game.map import Map
from game.tiles import TileDB


def new_actor(world: ComponentDict, components: Iterable[object] = ()) -> ComponentDict:
    ctx = world[Context]
    actor = ComponentDict([Position(0, 0), Graphic(), *components])
    ctx.actors.add(actor)
    actor.set(ctx.sched.schedule(0, actor))
    return actor


def get_memory(world: ComponentDict, actor: ComponentDict) -> MemoryLayer:
    """Return the actors memory of the active map."""
    active_map = world[Context].active_map
    if Memory not in actor:
        actor[Memory] = Memory()
    memory = actor[Memory]
    if active_map not in memory.layers:
        memory.layers[active_map] = MemoryLayer(
            tiles=np.zeros_like(active_map[Map][game.map_attrs.a_tiles]),
            objs={},
        )
    return memory.layers[active_map]


def compute_fov(world: ComponentDict, actor: ComponentDict, update_memory: bool = True) -> ActiveFOV:
    """Lazy compute the visible area from an actor and return the result.

    If `update_memory` is True then commit the viewed objects to memory.
    """
    active_map = world[Context].active_map
    actor_pos = actor[Position]
    fov = actor.get(ActiveFOV)
    if fov and fov.active_map is active_map and fov.active_pos == actor_pos:
        return fov

    tile_db = world[TileDB]
    transparency = tile_db.data["transparent"][active_map[Map][game.map_attrs.a_tiles]]
    fov = ActiveFOV(
        visible=tcod.map.compute_fov(
            transparency=transparency, pov=actor_pos.yx, radius=10, algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
        ),
        active_map=active_map,
        active_pos=actor_pos,
    )
    if update_memory:
        memory = get_memory(world, actor)
        memory.tiles = np.where(fov.visible, active_map[Map][game.map_attrs.a_tiles], memory.tiles)

        for old_pos in list(memory.objs.keys()):
            if fov.visible[old_pos.yx]:
                del memory.objs[old_pos]

        for obj in itertools.chain(
            world[Context].active_map[MapFeatures].features,
            world[Context].actors,
        ):
            pos = obj[Position]
            if fov.visible[pos.yx]:
                memory.objs[pos] = obj

    actor[ActiveFOV] = fov
    return fov
