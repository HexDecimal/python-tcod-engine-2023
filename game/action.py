from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

import attrs
from tcod.ec import ComponentDict


class Action:
    def __init__(self, data: Iterable[object]) -> None:
        self.data = ComponentDict(data)

    def poll(self, world: ComponentDict, actor: ComponentDict) -> PollResult:
        """Check if an action can be done.  Return the action to execute if it can."""
        return self

    def execute(self, world: ComponentDict, actor: ComponentDict) -> Success:
        """Force this action to be performed."""
        raise NotImplementedError()

    def perform(self, world: ComponentDict, actor: ComponentDict) -> ActionResult:
        result = self.poll(world, actor)
        if not isinstance(result, Action):
            return result
        assert result.poll(world, actor) is result
        return result.execute(world, actor)


@attrs.define()
class Success:
    time_passed: int


@attrs.define()
class Impossible:
    reason: str

    def __bool__(self) -> Literal[False]:
        return False


PollResult = Action | Impossible
ActionResult = Success | Impossible
