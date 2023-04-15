from collections.abc import Iterator
from typing import NamedTuple

from tcod.ec import ComponentDict

import game.actor_tools
import game.map_tools
from game.action import Action, Impossible, PollResult, Success
from game.components import Context, Direction, MapFeatures, Player, Position, Stairway
from game.map import Map, MapKey
from game.map_attrs import a_tiles
from game.tiles import TileDB


class Move(Action):
    def poll(self, world: ComponentDict, actor: ComponentDict) -> PollResult:
        context = world[Context]
        dest = actor[Position] + self.data[Direction]
        active_map = context.active_map[Map]
        if not (0 <= dest.x < active_map.width and 0 <= dest.y < active_map.height):
            return Impossible("Blocked.")
        if world[TileDB].data["walk_cost"][active_map[a_tiles][dest.yx]] > 0:
            return self
        return Impossible("Blocked.")

    def execute(self, world: ComponentDict, actor: ComponentDict) -> Success:
        dest = actor[Position] + self.data[Direction]
        actor[Position] = dest
        if Player in actor:
            game.actor_tools.compute_fov(world, actor)
        return Success(time_passed=100)


class Bump(Action):
    def poll(self, world: ComponentDict, actor: ComponentDict) -> PollResult:
        return Move([self.data[Direction]]).poll(world, actor)


class UseStairs(Action):
    class PassageInfo(NamedTuple):
        entrance: ComponentDict
        exit: ComponentDict
        next_map: MapKey

    def iter_stairs(self, map: ComponentDict) -> Iterator[ComponentDict]:
        for obj in map[MapFeatures].features:
            if Stairway not in obj:
                continue
            yield obj

    def get_stairs(self, world: ComponentDict, actor: ComponentDict) -> PassageInfo | None:
        actor_pos = actor[Position]
        inverse_dir = {"up": "down", "down": "up"}[self.data[str]]
        for stairs in self.iter_stairs(world[Context].active_map):
            if stairs[Position] != actor_pos:
                continue
            next_map_key = stairs[Stairway].up if self.data[str] == "up" else stairs[Stairway].down
            if next_map_key is None:
                continue
            for exit_passage in self.iter_stairs(game.map_tools.get_map(world, next_map_key)):
                print(exit_passage[Stairway])
                if getattr(exit_passage[Stairway], inverse_dir) is None:
                    continue
                return self.PassageInfo(stairs, exit_passage, next_map_key)
        return None

    def poll(self, world: ComponentDict, actor: ComponentDict) -> PollResult:
        if not self.get_stairs(world, actor):
            return Impossible("No stairs in that direction.")
        return self

    def execute(self, world: ComponentDict, actor: ComponentDict) -> Success:
        passage = self.get_stairs(world, actor)
        assert passage
        actor[Position] = passage.exit[Position]
        game.map_tools.activate_map(world, passage.next_map)
        return Success(time_passed=100)
