from enum import Enum
from dataclasses import dataclass

class PointsType(str, Enum):
    CURRENCY = "currency"
    ATTRIBUTE = "attribute"
    SKILL = "skill"

@dataclass
class Points:
    name: str
    label: str
    type: PointsType
    value: float
