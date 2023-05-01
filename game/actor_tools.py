import itertools
from collections.abc import Iterable

import numpy as np
import tcod
import tcod.map
from tcod.ecs import Entity, World

import game.map_attrs
from game.actor_types import ActiveFOV, Memory, MemoryLayer
from game.components import Context, Graphic, Position
from game.map import Map
from game.sched import Ticket
from game.tags import IsActor
from game.tiles import TileDB


def new_actor(parent: Entity, components: Iterable[object] = ()) -> Entity:
    """Spawn a new actor with the given components."""
    world = parent.world
    ctx = world.global_.components[Context]
    actor = world.new_entity([Position(0, 0), Graphic(), *components])
    actor.components[Ticket] = ctx.sched.schedule(0, actor)
    actor.tags.add(IsActor)
    actor.relation_tags["ChildOf"] = parent
    return actor


def get_memory(world: World, actor: Entity) -> MemoryLayer:
    """Return the actors memory of the active map."""
    active_map = world.global_.components[Context].active_map
    if Memory not in actor.components:
        actor.components[Memory] = Memory()
    memory = actor.components[Memory]
    if active_map not in memory.layers:
        memory.layers[active_map] = MemoryLayer(
            tiles=np.zeros_like(active_map.components[Map][game.map_attrs.a_tiles]),
            objs={},
        )
    return memory.layers[active_map]


def compute_fov(world: World, actor: Entity, update_memory: bool = True) -> ActiveFOV:
    """Lazy compute the visible area from an actor and return the result.

    If `update_memory` is True then commit the viewed objects to memory.
    """
    active_map = world.global_.components[Context].active_map
    actor_pos = actor.components[Position]
    fov = actor.components.get(ActiveFOV)
    if fov and fov.active_map is active_map and fov.active_pos == actor_pos:
        return fov

    tile_db = world.global_.components[TileDB]
    transparency = tile_db.data["transparent"][active_map.components[Map][game.map_attrs.a_tiles]]
    fov = ActiveFOV(
        visible=tcod.map.compute_fov(
            transparency=transparency, pov=actor_pos.yx, radius=10, algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
        ),
        active_map=active_map,
        active_pos=actor_pos,
    )
    if update_memory:
        memory = get_memory(world, actor)
        memory.tiles = np.where(fov.visible, active_map.components[Map][game.map_attrs.a_tiles], memory.tiles)

        for old_pos in list(memory.objs.keys()):
            if fov.visible[old_pos.yx]:
                del memory.objs[old_pos]

        for obj in itertools.chain(
            world.Q.all_of([Position], relations=[("ChildOf", active_map)]),
        ):
            pos = obj.components[Position]
            if fov.visible[pos.yx]:
                memory.objs[pos] = obj

    actor.components[ActiveFOV] = fov
    return fov
