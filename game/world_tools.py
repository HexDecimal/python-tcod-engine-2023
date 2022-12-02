from game.actor_tools import new_actor
from game.components import Context, Graphic, Player, Position
from game.entity import Entity
from game.map_tools import new_map


def new_world() -> Entity:
    world = Entity(Context())
    ctx = world[Context]
    ctx.active_map = new_map(50, 50)
    ctx.player = new_actor(world, (Position(1, 1), Graphic(ord("@")), Player()))
    return world
