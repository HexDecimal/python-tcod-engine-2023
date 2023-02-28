import attrs


@attrs.define
class Message:
    text: str
    count: int = 1

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text


@attrs.define
class MessageLog:
    log: list[Message] = attrs.field(factory=list)

    def append(self, text: str) -> None:
        if self.log and self.log[-1].text == text:
            self.log[-1].count += 1
            return
        self.log.append(Message(text))
