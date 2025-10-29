from dataclasses import dataclass
from typing import Optional

@dataclass
class Process:
    pid: str
    burst_time: int
    arrival_time: int = 0
    remaining_time: Optional[int] = None
    completion_time: Optional[int] = None
    start_time: Optional[int] = None

    def __post_init__(self):
        self.remaining_time = self.burst_time
        