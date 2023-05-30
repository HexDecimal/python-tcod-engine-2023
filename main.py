#!/usr/bin/env python
"""Main script entry point."""
import logging
import sys
import warnings

import tcod.context
import tcod.tileset

import g
import game.state
import game.states
import game.world_logic
import game.world_tools


def handle_state(result: game.state.StateResult) -> None:
    """Apply StateResult effects."""
    match result:
        case game.state.Push(state):
            g.state.append(state)
        case game.state.Pop():
            g.state.pop()
        case game.state.Reset(state):
            g.state = [state]
        case None:
            pass
        case _:
            raise AssertionError()
    if hasattr(g, "world"):
        game.world_logic.until_player_turn(g.world)


def main() -> None:
    """Program entry point."""
    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new(
        tileset=tileset,
        width=1280,
        height=720,
        title=None,
        vsync=True,
    ) as g.context:
        g.world = game.world_tools.new_world()
        g.state = [game.states.MainMenu()]
        while True:
            console = g.context.new_console(30, 20)
            g.state[-1].on_draw(console)
            g.context.present(console, keep_aspect=True, integer_scaling=True)
            for event in tcod.event.wait():
                event = g.context.convert_event(event)
                handle_state(g.state[-1].on_event(event))


if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
        if not sys.warnoptions:
            warnings.simplefilter("default")
    main()
