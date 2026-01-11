from dataclasses import dataclass

from .membership import Membership

@dataclass
class Character:
    id: int
    vk_id: int
    name: str
    age: int
    factions: list[Membership]

class CharactersRegistry:
    def get_all(self) -> list[Character]:
        return []

    def get_by_id(self, character_id: int) -> Character | None:
        pass
