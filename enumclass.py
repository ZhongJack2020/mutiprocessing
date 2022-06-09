from enum import Enum

class RFIDStatus(Enum):
    ERROR = 0
    FREE = 1
    BUSY = 2
    BUSY_FOR_USER = 3
    BUSY_FOR_SERVER = 4
    
class LockStatus(Enum):
    UNLOCK_REQ = 0
    CHECKING = 1
    UNLOCKING = 2
    UNLOCKED = 3

class Request(Enum):
    LOCK_UNLOCK = 0
    NW_CHECK = 1

class Respond(Enum):
    YES = 0