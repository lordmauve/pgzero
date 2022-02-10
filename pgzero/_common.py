from typing import Sequence, Tuple, Union, List
from pygame import Vector2, Rect
from .rect import ZRect

_Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]
_CanBeRect = Union[
    ZRect,
    Rect,
    Tuple[int, int, int, int],
    List[int],
    Tuple[_Coordinate, _Coordinate],
    List[_Coordinate],
]
