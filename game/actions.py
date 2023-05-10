"""Specialized common actions."""
import random
from collections.abc import Iterator
from typing import NamedTuple

from tcod.ecs import Entity

import game.actor_tools
import game.map_tools
from game.action import Action, Impossible, PlanResult, Success
from game.components import Context, Direction, Position, Stairway
from game.map import Map, MapKey
from game.map_attrs import a_tiles
from game.tags import ChildOf, IsPlayer
from game.tiles import TileDB


class Move(Action):
    """Move to an adjacent free space."""

    def plan(self, actor: Entity) -> PlanResult:
        world = actor.world
        context = world.global_.components[Context]
        dest = actor.components[Position] + self.data[Direction]
        active_map = context.active_map.components[Map]
        if not (0 <= dest.x < active_map.width and 0 <= dest.y < active_map.height):
            return Impossible("Blocked.")
        if world.global_.components[TileDB].data["walk_cost"][active_map[a_tiles][dest.yx]] > 0:
            return self
        return Impossible("Blocked.")

    def execute(self, actor: Entity) -> Success:
        dest = actor.components[Position] + self.data[Direction]
        actor.components[Position] = dest
        if IsPlayer in actor.tags:
            game.actor_tools.compute_fov(actor)
        return Success(time_passed=100)


class Bump(Action):
    """Context sensitive directional action."""

    def plan(self, actor: Entity) -> PlanResult:
        return Move([self.data[Direction]]).plan(actor)


class UseStairs(Action):
    class PassageInfo(NamedTuple):
        entrance: Entity
        exit: Entity
        next_map: MapKey

    def iter_stairs(self, map: Entity) -> Iterator[Entity]:
        yield from map.world.Q.all_of([Stairway], relations=[(ChildOf, map)])

    def get_stairs(self, actor: Entity) -> PassageInfo | None:
        world = actor.world
        actor_pos = actor.components[Position]
        inverse_dir = {"up": "down", "down": "up"}[self.data[str]]
        for stairs in self.iter_stairs(world.global_.components[Context].active_map):
            if stairs.components[Position] != actor_pos:
                continue
            next_map_key = (
                stairs.components[Stairway].up if self.data[str] == "up" else stairs.components[Stairway].down
            )
            if next_map_key is None:
                continue
            for exit_passage in self.iter_stairs(game.map_tools.get_map(world, next_map_key)):
                print(exit_passage.components[Stairway])
                if getattr(exit_passage.components[Stairway], inverse_dir) is None:
                    continue
                return self.PassageInfo(stairs, exit_passage, next_map_key)
        return None

    def plan(self, actor: Entity) -> PlanResult:
        if not self.get_stairs(actor):
            return Impossible("No stairs in that direction.")
        return self

    def execute(self, actor: Entity) -> Success:
        passage = self.get_stairs(actor)
        assert passage
        actor.components[Position] = passage.exit.components[Position]
        actor.relation_tags[ChildOf] = game.map_tools.activate_map(actor.world, passage.next_map)
        return Success(time_passed=100)


class RandomWalk(Action):
    def plan(self, actor: Entity) -> PlanResult:
        return Bump([Direction(random.randint(-1, 1), random.randint(-1, 1))]).plan(actor)
