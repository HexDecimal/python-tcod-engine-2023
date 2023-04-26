from weakref import WeakKeyDictionary

import attrs
import numpy as np
from numpy.typing import NDArray
from tcod.ecs import Entity

from game.components import Position


@attrs.define()
class MemoryLayer:
    tiles: NDArray[np.intc]
    objs: dict[Position, Entity]


@attrs.define()
class Memory:
    layers: WeakKeyDictionary[Entity, MemoryLayer] = attrs.field(factory=WeakKeyDictionary)


@attrs.define()
class ActiveFOV:
    visible: NDArray[np.bool_]
    active_map: Entity
    active_pos: Position
