"""Combat tools and logic."""
from tcod.ecs import Entity

from game.components import Graphic
from game.sched import Ticket
from game.tags import IsActor, IsPlayer


def kill(actor: Entity) -> None:
    """Invoke on-death logic for an actor."""
    print(f"{actor} dies.")
    del actor.components[Ticket]
    actor.tags.remove(IsActor)
    actor.components[Graphic] = Graphic(ord("%"), (127, 16, 16))
    if IsPlayer in actor.tags:
        msg = "Player has died."
        raise SystemExit(msg)
