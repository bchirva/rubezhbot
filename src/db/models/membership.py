from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..base_model import BaseModel


# pylint: disable=too-few-public-methods
class MembershipOrm(BaseModel):
    __tablename__ = "memberships"

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))
    fraction_id: Mapped[int] = mapped_column(ForeignKey("fractions.id"))
    rank: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)
    primary: Mapped[bool] = mapped_column(Boolean)
