from sqlalchemy import Float, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base_model import BaseModel


# pylint: disable=too-few-public-methods
class PointsOrm(BaseModel):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(2))

class CharacterPointsOrm(BaseModel):
    __tablename__ = "character_points"

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id")) 
    value: Mapped[float] = mapped_column(Float)
