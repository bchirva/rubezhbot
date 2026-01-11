from sqlalchemy.orm import Session

from ...domain.points import PointsType
from ..base_model import BaseModel
from ..engine import db_engine
from ..models import FractionOrm, PointsOrm, RankOrm


def seed_fraction(name: str, logo: str, ranks: list[str]):
    fraction = FractionOrm(name=name, logo=logo)

    with Session(db_engine) as s:
        s.add(fraction)
        s.flush()

        ranks_orm: list[RankOrm] = []
        for idx, rank_data in ranks:
            ranks_orm.append(
                RankOrm(fraction_id=fraction.id, level=idx, name=rank_data)
            )
        s.add_all(ranks_orm)
        s.commit()


BaseModel.metadata.create_all(bind=db_engine)

seed_fraction(
    name="Центр",
    logo="👮",
    ranks=["Кадет", "Фанрик", "Лейтенант", "Капитан", "Майор", "Полковник", "Генерал"],
)

seed_fraction(
    name="Синдикат",
    logo="🥷",
    ranks=[
        "Соучастник",
        "Двигатель",
        "Солдат",
        "Капитан",
        "Младший босс",
        "Советник",
        "Босс",
    ],
)

seed_fraction(
    name="Орден",
    logo="🎖️",
    ranks=[
        "Новобранец",
        "Вербовщик",
        "Шпион",
        "Капитан",
        "Планировщик",
        "Командующий",
        "Лидер",
    ],
)

seed_fraction(
    name="Церковь",
    logo="⛪",
    ranks=[
        "Кандидат",
        "Посвященный",
        "Адепт",
        "Знающий",
        "Хранитель",
        "Мастер пути",
        "Магистр",
    ],
)

seed_fraction(
    name="Мирные",
    logo="🛠️",
    ranks=[
        "Разнорабочий",
        "На кассе",
        "Первые заказы",
        "Майн крафт",
        "Лавочник",
        "Владелец предприятия",
        "Сетевой магнат",
    ],
)


with Session(db_engine) as session:
    attributes = [
        PointsOrm(name="Деньги", icon="💰", type=PointsType.CURRENCY),
        PointsOrm(name="Репутация", icon="🏅", type=PointsType.CURRENCY),
        PointsOrm(name="Сила", icon="💪", type=PointsType.ATTRIBUTE),
        PointsOrm(name="Ловкость", icon="👣", type=PointsType.ATTRIBUTE),
        PointsOrm(name="Выносливость", icon="🫀", type=PointsType.ATTRIBUTE),
        PointsOrm(name="Интеллект", icon="🧠", type=PointsType.ATTRIBUTE),
        PointsOrm(name="Харизма", icon="🔥", type=PointsType.ATTRIBUTE),
        PointsOrm(name="Мудрость", icon="☝️", type=PointsType.ATTRIBUTE),
    ]
    session.add_all(attributes)
    session.commit()
