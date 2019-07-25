from enum import Enum, auto


class MoveCategory(Enum):
    """Enum that represents a move type"""
    Status = auto()
    Physical = auto()
    Special = auto()


class MoveStatus(Enum):
    Locked = auto()
    Available = auto()
