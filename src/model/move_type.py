from enum import Enum, auto


class MoveCategory(Enum):
    Status = auto()
    Physical = auto()
    Special = auto()


class MoveStatus(Enum):
    Locked = auto()
    Available = auto()
