from typing import Iterable

from game.components import Context, Graphic, Position
from game.entity import Entity
from game.sched import Ticket


def new_actor(world: Entity, components: Iterable[object] = ()) -> Entity:
    ctx = world[Context]
    actor = Entity(*components)
    if Position not in actor:
        actor[Position] = Position(0, 0)
    if Graphic not in actor:
        actor[Graphic] = Graphic()
    ctx.actors.append(actor)
    actor[Ticket] = ctx.sched.schedule(0, actor)
    return actor
