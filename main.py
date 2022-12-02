#!/usr/bin/env python
import logging

import tcod

import g
import game.states
import game.world_logic
import game.world_tools


def main() -> None:
    tileset = tcod.tileset.load_tilesheet("data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    with tcod.context.new(
        tileset=tileset,
        width=1280,
        height=720,
        title=None,
        vsync=True,
    ) as g.context:
        g.world = game.world_tools.new_world()
        g.state = game.states.InGame()
        while True:
            console = g.context.new_console()
            g.state.on_draw(console)
            g.context.present(console, keep_aspect=True, integer_scaling=True)
            for event in tcod.event.wait():
                g.state.on_event(event)
                game.world_logic.until_player_turn(g.world)


if __name__ == "__main__":
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    main()
