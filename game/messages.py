"""Message log management."""
import attrs


@attrs.define
class Message:
    """A single or stacked message instance."""

    text: str
    count: int = 1

    def __str__(self) -> str:
        """Return this message."""
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text


@attrs.define
class MessageLog:
    """The active message log."""

    log: list[Message] = attrs.field(factory=list)

    def append(self, text: str) -> None:
        """Add or stack a new message."""
        if self.log and self.log[-1].text == text:
            self.log[-1].count += 1
            return
        self.log.append(Message(text))
