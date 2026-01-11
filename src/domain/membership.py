from dataclasses import dataclass, field

from .fraction import Fraction, Rank


@dataclass
class Membership:
    fraction: Fraction = field(default=Fraction())
    rank: Rank = field(default=Rank())
    comment: str = field(default="")
