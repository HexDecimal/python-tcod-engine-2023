from weakref import WeakKeyDictionary

import attrs
import numpy as np
from numpy.typing import NDArray
from tcod.ec import ComponentDict

from game.components import Position


@attrs.define()
class MemoryLayer:
    tiles: NDArray[np.intc]
    objs: dict[Position, ComponentDict]


@attrs.define()
class Memory:
    layers: WeakKeyDictionary[ComponentDict, MemoryLayer] = attrs.field(factory=WeakKeyDictionary)


@attrs.define()
class ActiveFOV:
    visible: NDArray[np.bool_]
    active_map: ComponentDict
    active_pos: Position
