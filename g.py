"""Explicitly mutable global names."""

import tcod.context
import tcod.ecs

import game.state

context: tcod.context.Context
state: list[game.state.State]
world: tcod.ecs.World
