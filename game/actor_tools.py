from typing import Iterable

from tcod.ec import ComponentDict

from game.components import Context, Graphic, Position


def new_actor(world: ComponentDict, components: Iterable[object] = ()) -> ComponentDict:
    ctx = world[Context]
    actor = ComponentDict([Position(0, 0), Graphic(), *components])
    ctx.actors.add(actor)
    actor.set(ctx.sched.schedule(0, actor))
    return actor
