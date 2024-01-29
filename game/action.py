"""The base class for actions are defined here."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

import attrs
from tcod.ec import ComponentDict
from tcod.ecs import Entity


class Action:
    """An action which can be planned and can possibly be executed."""

    def __init__(self, data: Iterable[object] = ()) -> None:
        """Construct an action with any relevant extra data."""
        self.data = ComponentDict(data)

    def plan(self, actor: Entity) -> PlanResult:
        """Check if an action can be done.  Return the action to execute if it can."""
        return self

    def execute(self, actor: Entity) -> Success:
        """Force this action to be performed."""
        raise NotImplementedError()

    def perform(self, actor: Entity) -> ActionResult:
        """Plan and execute an action."""
        result = self.plan(actor)
        if not isinstance(result, Action):
            return result
        assert result.plan(actor) is result, f"Planning was not finished, make sure plan is called on {result}."
        return result.execute(actor)


@attrs.define()
class Success:
    """Results of a successful action."""

    time_passed: int


@attrs.define()
class Impossible:
    """Action can not be performed."""

    reason: str

    def __bool__(self) -> Literal[False]:
        """Treat Impossible results as falsy."""
        return False


PlanResult = Action | Impossible
ActionResult = Success | Impossible
