from game.components import Context, Player
from game.entity import Entity
from game.sched import Ticket


def until_player_turn(world: Entity) -> None:
    ctx = world[Context]
    while True:
        next_ticket = ctx.sched.peek()
        entity = next_ticket.value
        assert isinstance(entity, Entity)
        if next_ticket is not entity[Ticket]:
            ctx.sched.pop()
            continue
        if Player in entity:
            return
