from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..base_model import BaseModel


# pylint: disable=too-few-public-methods
class FractionOrm(BaseModel):
    __tablename__ = "fractions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    logo: Mapped[str] = mapped_column(String(2))

    def __repr__(self) -> str:
        return f"{self.name}"


class RankOrm(BaseModel):
    __tablename__ = "ranks"

    fraction_id: Mapped[int] = mapped_column(ForeignKey("fractions.id"))
    level: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
