from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..base_model import BaseModel


# pylint: disable=too-few-public-methods
class CharacterOrm(BaseModel):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    age: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return f"#{self.id}: {self.name} (vk={self.vk_id})"
