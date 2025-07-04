from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class Item(Base):
    __tablename__ = 'apeiros_items'

    # Interal id for this type of item
    item_id: Mapped[str] = mapped_column(primary_key=True)

    # Details
    name: Mapped[str]
    description: Mapped[str]

    def __repr__(self):
        return (
            f'Item(id={self.item_id!r}, name={self.name!r}, description={self.description!r})'
        )
