from enum import Enum, auto


class AgentStatus(Enum):
    COMPLETED = auto()
    ERROR_PAUSED = auto()
    PAUSED = auto()
    RUNNING = auto()
