"""The State base class is defined here."""

from __future__ import annotations

from typing import Protocol

import attrs
import tcod.console
import tcod.event


class State(Protocol):
    """A state machine dispatch class. Subclasses define what a state does."""

    def on_event(self, event: tcod.event.Event) -> StateResult:
        """Handle an event and return a value which may affect the active state."""

    def on_draw(self, console: tcod.console.Console) -> None:
        """Visualize this state onto the given console."""


@attrs.define(frozen=True)
class Push:
    """Push a new state on top of the stack."""

    state: State


@attrs.define(frozen=True)
class Pop:
    """Pop the top state off the stack, usually means the current state."""


@attrs.define(frozen=True)
class Reset:
    """Delete the stack and replace it with a new state."""

    state: State


StateResult = Push | Pop | Reset | None
"""Common return values for State dispatch functions."""
