from typing import Iterator

from tcod.ec import ComponentDict

import game.actor_tools
import game.map_tools
from game.action import Action, ActionResult, Impossible, Success
from game.components import Context, Direction, MapFeatures, Player, Position, Stairway
from game.map import Map
from game.map_attrs import a_tiles
from game.tiles import TileDB


class Bump(Action):
    def perform(self, world: ComponentDict, actor: ComponentDict) -> ActionResult:
        context = world[Context]
        dest = actor[Position] + self.data[Direction]
        if world[TileDB].data["walk_cost"][context.active_map[Map][a_tiles][dest.yx]] > 0:
            actor[Position] = dest
            if Player in actor:
                game.actor_tools.compute_fov(world, actor)
            return Success(time_passed=100)
        return Impossible("Blocked.")


class UseStairs(Action):
    def iter_stairs(self, map: ComponentDict) -> Iterator[ComponentDict]:
        for obj in map[MapFeatures].features:
            if Stairway not in obj:
                continue
            yield obj

    def perform(self, world: ComponentDict, actor: ComponentDict) -> ActionResult:
        actor_pos = actor[Position]
        assert self.data[str] in {"up", "down"}

        for stairs in self.iter_stairs(world[Context].active_map):
            if stairs[Position] != actor_pos:
                continue
            next_map = stairs[Stairway].up if self.data[str] == "up" else stairs[Stairway].down

            if next_map is None:
                continue
            inverse_dir = {"up": "down", "down": "up"}[self.data[str]]
            for dest_stairs in self.iter_stairs(game.map_tools.get_map(world, next_map)):
                print(dest_stairs[Stairway])
                if getattr(dest_stairs[Stairway], inverse_dir) is None:
                    continue
                actor[Position] = dest_stairs[Position]
                break

            game.map_tools.activate_map(world, next_map)
            return Success(time_passed=100)

        return Impossible("No stairs in that direction.")
