import heapq
from typing import Generic, Iterable, NamedTuple, TypeVar

T = TypeVar("T")


class Ticket(NamedTuple, Generic[T]):
    time: int
    uid: int
    value: T
    insert_time: int


class TurnQueue(Generic[T]):
    def __init__(self, *, time: int = 0, next_uid: int = 0, heap: Iterable[Ticket[T]] = ()) -> None:
        self.time = time
        self.next_uid = next_uid
        self.heap = list(heap)
        heapq.heapify(self.heap)

    def schedule(self, interval: int, value: T) -> Ticket[T]:
        ticket = Ticket(self.time + interval, self.next_uid, value, self.time)
        self.next_uid += 1
        heapq.heappush(self.heap, ticket)
        return ticket

    def peek(self) -> Ticket[T]:
        self.time = self.heap[0].time
        return self.heap[0]

    def pop(self) -> Ticket[T]:
        ticket = heapq.heappop(self.heap)
        self.time = ticket.time
        return ticket
