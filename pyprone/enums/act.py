from enum import Enum

class Commands(Enum):
    """ command enum """
    # entity based command
    PRTEXT_APPEND_TEXT = 1
    PRTEXT_CLEAR = 2

    # cross entity command
    BROADCAST_TEXT = 1001

    # system command
    SYSTEM_EXIT = 10000