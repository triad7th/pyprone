from enum import Enum

class WnPos(Enum):
    NONE = 0
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4

class WnStatus(Enum):
    NONE = 0
    MAXIMIZED = 1
    MINIMIZED = 2
