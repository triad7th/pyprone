from enum import Enum

class PrCmds(Enum):
    """ command enum """
    # entity based command
    PRTEXT_APPEND_TEXT = 1
    PRTEXT_BACK_TEXT = 2
    PRTEXT_CLEAR = 3

    # cross entity command
    BROADCAST_TEXT = 1001
    BROADCAST_ENTITY_LIST = 1002

    # system command
    SYSTEM_EXIT = 10000
