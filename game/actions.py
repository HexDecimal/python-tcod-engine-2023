"""Specialized common actions."""
import random
from typing import NamedTuple

from tcod.ecs import Entity

import game.actor_tools
import game.combat
import game.map_tools
from game.action import Action, Impossible, PlanResult, Success
from game.components import Context, Direction, Position, Stairway
from game.map import Map, MapKey
from game.map_attrs import a_tiles
from game.tags import ChildOf, IsActor, IsPlayer
from game.tiles import TileDB


class Move(Action):
    """Move to an adjacent free space."""

    def plan(self, actor: Entity) -> PlanResult:
        world = actor.world
        context = world[None].components[Context]
        dest = actor.components[Position] + self.data[Direction]
        active_map = context.active_map.components[Map]
        if not (0 <= dest.x < active_map.width and 0 <= dest.y < active_map.height):
            return Impossible("Blocked.")
        if world[None].components[TileDB].data["walk_cost"][active_map[a_tiles][dest.yx]] > 0:
            return self
        return Impossible("Blocked.")

    def execute(self, actor: Entity) -> Success:
        dest = actor.components[Position] + self.data[Direction]
        actor.components[Position] = dest
        if IsPlayer in actor.tags:
            game.actor_tools.compute_fov(actor)
        return Success(time_passed=100)


class Melee(Action):
    """Melee attack target."""

    def plan(self, actor: Entity) -> PlanResult:
        direction = self.data[Entity].components[Position] - actor.components[Position]
        if min(abs(direction.x), abs(direction.y)) > 1:
            return Impossible("Target is out of range.")
        return self

    def execute(self, actor: Entity) -> Success:
        target = self.data[Entity]
        damage = actor.components[("attack", int)]
        print(f"Attacking {target} for {damage} damage.")
        target.components[("hp", int)] -= damage
        if target.components[("hp", int)] < 0:
            game.combat.kill(target)
        return Success(time_passed=100)


class Bump(Action):
    """Context sensitive directional action."""

    def plan(self, actor: Entity) -> PlanResult:
        dest = actor.components[Position] + self.data[Direction]
        for target in actor.world.Q.all_of([Position], tags=[IsActor]):
            if target.components[Position] == dest and target is not actor:
                result = Melee([target]).plan(actor)
                if result:
                    return result
        return Move([self.data[Direction]]).plan(actor)


class UseStairs(Action):
    class PassageInfo(NamedTuple):
        entrance: Entity
        exit: Entity
        next_map: MapKey

    def get_stairs(self, actor: Entity) -> PassageInfo | None:
        world = actor.world
        inverse_dir = {"up": "down", "down": "up"}[self.data[str]]
        for stairs in world.Q.all_of(
            components=[Stairway],
            tags=[actor.components[Position]],
            relations=[(ChildOf, actor.relation_tag[ChildOf])],
        ):
            next_map_key = (
                stairs.components[Stairway].up if self.data[str] == "up" else stairs.components[Stairway].down
            )
            if next_map_key is None:
                continue
            for exit_passage in world.Q.all_of(
                components=[Stairway], relations=[(ChildOf, game.map_tools.get_map(world, next_map_key))]
            ):
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


class AttackPlayer(Action):
    """Seek and attack the player."""

    def plan(self, actor: Entity) -> PlanResult:
        """Bump towards the player actor."""
        my_fov = game.actor_tools.compute_fov(actor)
        targets = [
            target
            for target in actor.world.Q.all_of(
                components=[Position], tags=[IsPlayer], relations=[(ChildOf, actor.relation_tags[ChildOf])]
            )
            if my_fov.visible[target.components[Position].yx]
        ]
        if not targets:
            return Impossible("No visible targets.")
        target = targets[0]
        direction = (target.components[Position] - actor.components[Position]).chebyshev_normalize
        return Bump([Direction(*direction.xy)]).plan(actor)
