"""Tools for running world simulations."""
from tcod.ecs import Entity, World

from game.action import Action, Impossible, Success
from game.components import Context
from game.messages import MessageLog
from game.sched import Ticket


def until_player_turn(world: World) -> None:
    """Run scheduled entities in order until the player is next."""
    ctx = world.global_.components[Context]
    while True:
        next_ticket = ctx.sched.peek()
        entity = next_ticket.value
        assert isinstance(entity, Entity)
        if next_ticket is not entity.components.get(Ticket):  # Ticket is invalid (possibly rescheduled).
            ctx.sched.pop()
            continue
        if ("ai", Action) not in entity.components:
            return
        do_action(entity, entity.components[("ai", Action)])


def do_action(actor: Entity, action: Action) -> None:
    """Perform the given action on the given actor."""
    ctx = actor.world.global_.components[Context]
    is_player = ("ai", Action) not in actor.components
    match action.perform(actor):
        case Success(time_passed=time_passed):
            assert ctx.sched.peek() is actor.components[Ticket]
            ctx.sched.pop()
            actor.components[Ticket] = ctx.sched.schedule(time_passed, actor)
        case Impossible(reason=reason):
            if is_player:
                actor.world.global_.components[MessageLog].append(reason)
            else:
                ctx.sched.pop()
                actor.components[Ticket] = ctx.sched.schedule(100, actor)
        case _:
            raise NotImplementedError()
