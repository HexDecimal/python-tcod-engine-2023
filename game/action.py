from typing import Iterable

from tcod.ec import ComponentDict


class Action:
    def __init__(self, data: Iterable[object]) -> None:
        self.data = ComponentDict(data)

    def perform(self, world: ComponentDict, actor: ComponentDict) -> None:
        pass
