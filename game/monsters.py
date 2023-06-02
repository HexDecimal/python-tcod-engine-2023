"""Monster database manager."""
from __future__ import annotations

import tomllib
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import attrs
from tcod.ecs import Entity

from game.components import Context, Graphic, Position
from game.sched import Ticket
from game.tags import IsActor


def _convert_ch(value: str | int) -> int:
    """Convert value to an integer code point."""
    if isinstance(value, int):
        return value
    return ord(value)


def _convert_color(value: Iterable[int]) -> tuple[int, int, int]:
    """Convert value to an (r, g, b) tuple."""
    r, g, b = value
    return int(r), int(g), int(b)


@attrs.define(frozen=True)
class MonsterType:
    """A creature definition."""

    name: str = attrs.field(converter=str)
    ch: int = attrs.field(converter=_convert_ch)
    fg: tuple[int, int, int] = attrs.field(converter=_convert_color)
    hp: int = attrs.field(converter=int)
    attack: int = attrs.field(converter=int)


monster_db: dict[str, MonsterType] = {}
"""Monster database."""


def init() -> None:
    """Initialize the monster database."""
    data: dict[str, Any]
    for name, data in tomllib.loads(Path("data/monsters.toml").read_text(encoding="utf-8")).items():
        monster_db[name] = MonsterType(
            name=name,
            ch=data.pop("ch", "?"),
            fg=data.pop("fg", (255, 255, 255)),
            hp=data.pop("hp"),
            attack=data.pop("attack"),
        )
        assert not data, f"Unhandled data: {data}"


def spawn(race: str, parent: Entity, pos: Position) -> Entity:
    """Spawn a monster at the given location."""
    if not monster_db:
        init()
    race_info = monster_db[race]
    world = parent.world
    ctx = world.global_.components[Context]
    actor = world.new_entity(tags=[IsActor])
    actor.components.update(
        {
            Ticket: ctx.sched.schedule(0, actor),
            Position: pos,
            Graphic: Graphic(race_info.ch, race_info.fg),
            ("name", str): race_info.name,
            ("hp", int): race_info.hp,
            ("max_hp", int): race_info.hp,
            ("attack", int): race_info.attack,
        }
    )
    actor.relation_tags["ChildOf"] = parent
    return actor
