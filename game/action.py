from __future__ import annotations

from typing import Iterable

import attrs
from tcod.ec import ComponentDict


class Action:
    def __init__(self, data: Iterable[object]) -> None:
        self.data = ComponentDict(data)

    def perform(self, world: ComponentDict, actor: ComponentDict) -> ActionResult:
        raise NotImplementedError()


@attrs.define()
class Success:
    time_passed: int


@attrs.define()
class Impossible:
    reason: str


ActionResult = Success | Impossible
