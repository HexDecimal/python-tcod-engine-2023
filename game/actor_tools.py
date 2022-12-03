from typing import Iterable

from game.components import Context, Graphic, Position
from game.entity import Entity


def new_actor(world: Entity, components: Iterable[object] = ()) -> Entity:
    ctx = world[Context]
    actor = Entity(Position(0, 0), Graphic(), *components)
    ctx.actors.add(actor)
    actor.add(ctx.sched.schedule(0, actor))
    return actor
