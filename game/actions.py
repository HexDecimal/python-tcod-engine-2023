from tcod.ec import ComponentDict

from game.action import Action
from game.components import Context, Direction, Position
from game.map import Map
from game.map_attrs import a_tiles
from game.sched import Ticket
from game.tiles import tiles_db


class Bump(Action):
    def perform(self, world: ComponentDict, actor: ComponentDict) -> None:
        context = world[Context]
        dest = actor[Position] + self.data[Direction]
        if tiles_db["walk_cost"][context.active_map[Map][a_tiles][dest.yx]] > 0:
            actor[Position] = dest
            world[Context].player[Ticket] = world[Context].sched.schedule(100, world[Context].player)
