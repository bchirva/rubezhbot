from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.fraction import RankOrm

from ..db import db_engine
from ..db.models import FractionOrm


@dataclass
class Fraction:
    id: int = field(default=0)
    name: str = field(default="")
    logo: str = field(default="")


@dataclass
class Rank:
    level: int = field(default=0)
    name: str = field(default="")


class FractionsRegistry:
    def get_all(self) -> list[Fraction]:
        with Session(db_engine) as session:
            query = select(FractionOrm)
            fractions = session.scalars(query).all()

            result: list[Fraction] = []
            for fraction in fractions:
                result.append(
                    Fraction(id=fraction.id, name=fraction.name, logo=fraction.logo)
                )

            return result

    def get_by_id(self, fraction_id: int) -> Fraction | None:
        with Session(db_engine) as session:
            query = select(FractionOrm).where(FractionOrm.id == fraction_id)
            if (fraction := session.scalars(query).first()) is not None:
                return Fraction(id=fraction.id, name=fraction.name, logo=fraction.logo)

            return None

    def get_fraction_ranks(self, fraction_id: int) -> list[Rank]:
        with Session(db_engine) as session:
            query = select(RankOrm).where(RankOrm.fraction_id == fraction_id)
            ranks = session.scalars(query).all()

            result: list[Rank] = []
            for rank in ranks:
                result.append(Rank(level=rank.level, name=rank.name))

            return result

    def get_fraction_rank_level(self, fraction_id: int, rank_level: int) -> Rank | None:
        with Session(db_engine) as session:
            query = select(RankOrm).where(
                RankOrm.fraction_id == fraction_id and RankOrm.level == rank_level
            )
            if (rank := session.scalars(query).first()) is not None:
                return Rank(level=rank.level, name=rank.name)

            return None
