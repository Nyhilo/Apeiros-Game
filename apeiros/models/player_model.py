from typing import Optional, List, Dict, Any

from sqlalchemy import Table, Column, ForeignKey, BLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .medal_model import Medal
from .item_model import Item
from .nomster_model import Nomster


_player_medal_association_table = Table(
    "apeiros_player_medals",
    Base.metadata,
    Column("player_id", ForeignKey('apeiros_players.id')),
    Column("medal_id", ForeignKey('apeiros_medals.medal_id')),
)


class PlayerItem(Base):
    __tablename__ = 'apeiros_player_items'

    # Foreign Keys
    _player_id: Mapped[int] = mapped_column('player_id', ForeignKey('apeiros_players.id'), primary_key=True)
    _item_id: Mapped[str] = mapped_column('item_id', ForeignKey('apeiros_items.item_id'), primary_key=True)

    item: Mapped[Item] = relationship()

    # Inventory data
    amount: Mapped[int]

    def __repr__(self):
        return (
            f'Item(player={self._player_id!r}, item_id={self._item_id!r}, item={self.item!r}, amount={self.amount!r})'
        )


class Player(Base):
    __tablename__ = 'apeiros_players'

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Client specific unique id such as a discord user ID, or generated id
    # If no alternate unique id is available, this should be the same as username
    unique_id: Mapped[str]

    # User identifying names that will be rendered to the user
    username: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]]

    # A png byte blob
    player_token = mapped_column(type_=BLOB, nullable=True)

    # Medals owned by this player
    medals: Mapped[List[Medal]] = relationship(secondary=_player_medal_association_table)

    # Currency, in the form of points.
    points: Mapped[int]

    # Items owned by this player. This is a dictionary with item_ids as keys and the amount owned as values
    inventory: Mapped[List[PlayerItem]] = relationship()

    # The nomsters owned by this player
    nomsters: Mapped[List[Nomster]] = relationship(back_populates='owner', foreign_keys=Nomster.owner_id)

    # Public Methods #
    def add_item(self, item: Item):
        '''Add an item to the inventory or increment the amount of an existing item'''
        if existing := self.get_slot(item.item_id):
            existing.amount += 1
            return

        self.inventory.append(PlayerItem(_player_id=self.id, _item_id=item.item_id, item=item, amount=1))

    def remove_item(self, item: Item, amount: int = 1):
        '''Decrement the amount of an existing item and remove it if there are none left'''
        if existing := self.get_slot(item.item_id):
            existing.amount -= amount

            if existing.amount <= 0:
                self.inventory.remove(existing)

    def get_slot(self, item_id: str) -> PlayerItem:
        '''Returns the inventory slot for an item. Use slot.item to interrogate the item details'''
        for pItem in self.inventory:
            if pItem.item.item_id == item_id:
                return pItem

        return None

    @property
    def name(self) -> str:
        if self.nickname is not None:
            return self.nickname

        return self.username

    def __repr__(self) -> str:
        return (
            f'Player(id={self.id!r}, unique_id={self.unique_id!r}, username={self.username!r}, '
            f'nickname={self.nickname!r}, medals={self.medals!r}, points={self.points!r}, items={self.inventory!r})'
        )
