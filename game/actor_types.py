"""Classes related to actors."""

from weakref import WeakKeyDictionary

import attrs
import numpy as np
from numpy.typing import NDArray
from tcod.ecs import Entity

from game.components import Position


@attrs.define()
class MemoryLayer:
    """The recorded memory of a specific map."""

    tiles: NDArray[np.intc]
    objs: dict[Position, Entity]


@attrs.define()
class Memory:
    """The remembered entities and tiles of an actor."""

    layers: WeakKeyDictionary[Entity, MemoryLayer] = attrs.field(factory=WeakKeyDictionary)


@attrs.define(eq=False)
class ActiveFOV:
    """The current FOV of an actor."""

    visible: NDArray[np.bool_]
    active_map: Entity
    active_pos: Position
