import snecs_mod
from game.components import Globals, Position


def new_world() -> snecs_mod.WorldWithContext:
    world = snecs_mod.WorldWithContext()
    ctx = Globals()
    world.add_component(world.context, ctx)
    ctx.player = world.new_entity([Position(0, 0)])
    return world
