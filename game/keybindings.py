import enum
from collections import defaultdict
from collections.abc import Callable, Iterable
from typing import Any, Self, TypeVar

import attrs
import tcod.event
import toml  # type:ignore[import]

_Enum = TypeVar("_Enum", bound=enum.Enum)


_MOD_ENCODE = {
    None: "ignore",
    False: "false",
    True: "true",
    (False, False): "neither",
    (True, False): "left",
    (False, True): "right",
    (True, True): "both",
}

_MOD_DECODE = {v: k for k, v in _MOD_ENCODE.items()}


@attrs.define(frozen=True, kw_only=True)
class Bind:
    sym: tcod.event.KeySym | None = None
    scancode: tcod.event.Scancode | None = None
    shift: bool | tuple[bool, bool] | None = False
    alt: bool | tuple[bool, bool] | None = False
    ctrl: bool | tuple[bool, bool] | None = False
    gui: bool | tuple[bool, bool] | None = False
    mode: bool | None = False
    num_lock: bool | None = None
    caps_lock: bool | None = None
    scroll_lock: bool | None = None

    def __match_modifier(self, name: str, event: tcod.event.KeyboardEvent) -> bool:
        """Return True if the modifiers in `event` match `name` in this object.

        - self value is None: True is returned.
        - self value is bool: True if modifier matches.
        - self value is (bool, bool): True if modifier keys exactly match.
        """
        assert name != "shift"
        self_value: None | bool | tuple[bool, bool] = getattr(self, name)
        if self_value is None:
            return True
        upper_name = name.upper()
        if isinstance(self_value, bool):
            return self_value == bool(event.mod & getattr(tcod.event, f"KMOD_{upper_name}"))
        return self_value == (
            bool(event.mod & getattr(tcod.event, f"KMOD_L{upper_name}")),
            bool(event.mod & getattr(tcod.event, f"KMOD_R{upper_name}")),
        )

    @property
    def value(self) -> int:
        """The narrowness of this binding.

        High value means this bind is more specific and should take priority over other bindings.
        """
        return (
            0
            + (self.num_lock is not None)
            + (self.caps_lock is not None)
            + (self.scroll_lock is not None)
            + (self.mode is not None)
            + (self.shift is not None)
            + (self.alt is not None)
            + (self.ctrl is not None)
            + (self.gui is not None)
            + isinstance(self.shift, tuple)
            + isinstance(self.alt, tuple)
            + isinstance(self.ctrl, tuple)
            + isinstance(self.gui, tuple)
        )

    def match(self, event: tcod.event.Event, toggle_shift: bool) -> bool:
        """Return True if all non-None values match the attributes in `event`."""
        if not isinstance(event, tcod.event.KeyboardEvent):
            return False
        if self.sym is not None and self.sym != event.sym:
            return False
        if self.scancode is not None and self.scancode != event.scancode:
            return False
        if self.shift is not None:
            if isinstance(self.shift, bool):
                shift = event.mod & tcod.event.KMOD_SHIFT != 0
                shift ^= toggle_shift and (event.mod & tcod.event.KMOD_CAPS != 0)
                if self.shift != shift:
                    return False
            elif self.shift != (event.mod & tcod.event.KMOD_LSHIFT != 0, event.mod & tcod.event.KMOD_RSHIFT != 0):
                return False
        return (
            (self.mode is None or self.mode == (event.mod & tcod.event.KMOD_MODE != 0))
            and (self.num_lock is None or self.num_lock == (event.mod & tcod.event.KMOD_NUM != 0))
            and (self.caps_lock is None or self.caps_lock == (event.mod & tcod.event.KMOD_CAPS != 0))
            and (self.scroll_lock is None or self.scroll_lock == (event.mod & tcod.event.KMOD_SCROLL != 0))
            and self.__match_modifier("alt", event)
            and self.__match_modifier("ctrl", event)
            and self.__match_modifier("gui", event)
        )

    @classmethod
    def _from_toml_str(cls, state: dict[str, str]) -> Self:
        """Parse a TOML inline table and return a new Bind."""
        decode_keys: dict[str, Any] = {}
        if "sym" in state:
            decode_keys["sym"] = tcod.event.KeySym[state["sym"]]
            del state["sym"]
        if "scancode" in state:
            decode_keys["scancode"] = tcod.event.Scancode[state["scancode"]]
            del state["scancode"]
        return cls(
            **decode_keys,
            **{key: _MOD_DECODE[value] for key, value in state.items()},  # type: ignore[arg-type]
        )

    def _as_toml_str(self) -> str:
        """Export this Bind as an inline table for TOML."""
        state: dict[str, str | bool | tuple[bool, bool]] = {}
        if self.sym is not None:
            state["sym"] = self.sym.name
        if self.scancode is not None:
            state["scancode"] = self.scancode.name
        if self.shift is not False:
            state["shift"] = _MOD_ENCODE[self.shift]
        if self.alt is not False:
            state["alt"] = _MOD_ENCODE[self.alt]
        if self.ctrl is not False:
            state["ctrl"] = _MOD_ENCODE[self.ctrl]
        if self.gui is not False:
            state["gui"] = _MOD_ENCODE[self.gui]
        if self.mode is not False:
            state["mode"] = _MOD_ENCODE[self.mode]
        if self.num_lock is not None:
            state["num_lock"] = _MOD_ENCODE[self.num_lock]
        if self.caps_lock is not None:
            state["caps_lock"] = _MOD_ENCODE[self.caps_lock]
        if self.scroll_lock is not None:
            state["scroll_lock"] = _MOD_ENCODE[self.scroll_lock]
        output = []
        for key, value in state.items():
            output.append(f"{key} = {value!r}")
        return f"""{{ {", ".join(output)} }}"""


class Keybindings:
    def __init__(self) -> None:
        self.binds: dict[type[enum.Enum], dict[Bind, enum.Enum]] = defaultdict(dict)
        self.enums: dict[str, type[enum.Enum]] = {}
        self.toggle_shift = False

    def register(self, category: str | None = None) -> Callable[[type[_Enum]], type[_Enum]]:
        def func(__enum: type[_Enum]) -> type[_Enum]:
            self.binds[__enum] = {}
            self.enums[__enum.__name__] = __enum
            return __enum

        return func

    def loads(self, s: str) -> None:
        input = toml.loads(s)
        assert input["version"] == "0.0"
        del input["version"]
        for category, bindings in input.items():
            enum_type = self.enums[category]
            for name, binds in bindings.items():
                for bind in binds:
                    self.binds[enum_type][Bind._from_toml_str(bind)] = enum_type[name]

    def dumps(self) -> str:
        output: list[str] = ['version = "0.0"', ""]
        for enum_type, binds in self.binds.items():
            category = enum_type.__name__
            output.append(f"[{category}]")
            bindings: dict[str, list[str]] = {}
            for bind, value in binds.items():
                bindings.setdefault(value.name, []).append(bind._as_toml_str())
            for bind_name, bind_list in bindings.items():
                output.append(f"{bind_name} = [")
                for bind_str in bind_list:
                    output.append(f"    {bind_str},")
                output.append("]")
            output.append("")
        return "\n".join(output)

    def add_bind(self, enum: enum.Enum, bind: Bind) -> None:
        self.binds[type(enum)][bind] = enum

    def add_binds(self, bindings: dict[enum.Enum, Iterable[Bind]]) -> None:
        for value, binds in bindings.items():
            enum_type = type(value)
            for bind in binds:
                self.binds[enum_type][bind] = value

    def parse(self, event: tcod.event.Event, enum: type[_Enum]) -> _Enum | None:
        if not isinstance(event, tcod.event.KeyboardEvent):
            return None
        binds = self.binds[enum]
        for bind, value in sorted(binds.items(), key=lambda x: x[0].value, reverse=True):
            if bind.match(event, self.toggle_shift):
                assert isinstance(value, enum)
                return value
        return None
