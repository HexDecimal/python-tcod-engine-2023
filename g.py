import tcod
import tcod.ec

import game.state

context: tcod.context.Context
state: list[game.state.State]
world: tcod.ec.ComponentDict
