from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class Medal(Base):
    __tablename__ = 'apeiros_medals'

    # Interal id for this type of medal
    medal_id: Mapped[str] = mapped_column(primary_key=True)

    # Details
    name: Mapped[str]
    criteria: Mapped[str]
    number_available: Mapped[int]

    def __repr__(self):
        return (
            f'Medal(id={self.medal_id!r}, name={self.name!r}, criteria={self.criteria!r}, '
            f'number_available={self.number_available!r})'
        )
