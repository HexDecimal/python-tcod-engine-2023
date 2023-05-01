"""Tools for running world simulations."""
from tcod.ecs import Entity, World

from game.components import Context, Player
from game.sched import Ticket


def until_player_turn(world: World) -> None:
    """Run scheduled entities in order until the player is next."""
    ctx = world.global_.components[Context]
    while True:
        next_ticket = ctx.sched.peek()
        entity = next_ticket.value
        assert isinstance(entity, Entity)
        if next_ticket is not entity.components[Ticket]:  # Ticket is invalid (possibly rescheduled).
            ctx.sched.pop()
            continue
        if Player in entity.components:
            return
