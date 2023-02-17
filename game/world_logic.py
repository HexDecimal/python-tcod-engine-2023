from tcod.ec import ComponentDict

from game.components import Context, Player
from game.sched import Ticket


def until_player_turn(world: ComponentDict) -> None:
    ctx = world[Context]
    while True:
        next_ticket = ctx.sched.peek()
        entity = next_ticket.value
        assert isinstance(entity, ComponentDict)
        if next_ticket is not entity[Ticket]:  # Ticket is invalid (possibly rescheduled).
            ctx.sched.pop()
            continue
        if Player in entity:
            return
