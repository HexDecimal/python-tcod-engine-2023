from enum import Enum
from typing import NamedTuple

from tcod.event import KeySym

from game.keybindings import Bind, Keybindings

keybindings = Keybindings()


class MoveDir(NamedTuple):
    x: int
    y: int


@keybindings.register()
class InGame(Enum):
    MOVE_N = MoveDir(0, -1)
    MOVE_NE = MoveDir(1, -1)
    MOVE_E = MoveDir(1, 0)
    MOVE_SE = MoveDir(1, 1)
    MOVE_S = MoveDir(0, 1)
    MOVE_SW = MoveDir(-1, 1)
    MOVE_W = MoveDir(-1, 0)
    MOVE_NW = MoveDir(-1, -1)
    WAIT = "WAIT"


# Arrow keys.
keybindings.add_bind(InGame.MOVE_N, Bind(sym=KeySym.UP))
keybindings.add_bind(InGame.MOVE_S, Bind(sym=KeySym.DOWN))
keybindings.add_bind(InGame.MOVE_W, Bind(sym=KeySym.LEFT))
keybindings.add_bind(InGame.MOVE_E, Bind(sym=KeySym.RIGHT))
keybindings.add_bind(InGame.MOVE_NW, Bind(sym=KeySym.HOME))
keybindings.add_bind(InGame.MOVE_SW, Bind(sym=KeySym.END))
keybindings.add_bind(InGame.MOVE_NE, Bind(sym=KeySym.PAGEUP))
keybindings.add_bind(InGame.MOVE_SE, Bind(sym=KeySym.PAGEDOWN))

# Numpad keys.
keybindings.add_bind(InGame.MOVE_SW, Bind(sym=KeySym.KP_1))
keybindings.add_bind(InGame.MOVE_S, Bind(sym=KeySym.KP_2))
keybindings.add_bind(InGame.MOVE_SE, Bind(sym=KeySym.KP_3))
keybindings.add_bind(InGame.MOVE_W, Bind(sym=KeySym.KP_4))
keybindings.add_bind(InGame.MOVE_E, Bind(sym=KeySym.KP_6))
keybindings.add_bind(InGame.MOVE_NW, Bind(sym=KeySym.KP_7))
keybindings.add_bind(InGame.MOVE_N, Bind(sym=KeySym.KP_8))
keybindings.add_bind(InGame.MOVE_NE, Bind(sym=KeySym.KP_9))

# Vi keys.
keybindings.add_bind(InGame.MOVE_W, Bind(sym=KeySym.h))
keybindings.add_bind(InGame.MOVE_N, Bind(sym=KeySym.j))
keybindings.add_bind(InGame.MOVE_S, Bind(sym=KeySym.k))
keybindings.add_bind(InGame.MOVE_E, Bind(sym=KeySym.l))
keybindings.add_bind(InGame.MOVE_NW, Bind(sym=KeySym.y))
keybindings.add_bind(InGame.MOVE_NE, Bind(sym=KeySym.u))
keybindings.add_bind(InGame.MOVE_SW, Bind(sym=KeySym.b))
keybindings.add_bind(InGame.MOVE_SE, Bind(sym=KeySym.n))

keybindings.add_bind(InGame.WAIT, Bind(sym=KeySym.PERIOD))
keybindings.add_bind(InGame.WAIT, Bind(sym=KeySym.KP_5))
keybindings.add_bind(InGame.WAIT, Bind(sym=KeySym.CLEAR))
