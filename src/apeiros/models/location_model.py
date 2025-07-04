from typing import Optional, List

from sqlalchemy import ForeignKey, BLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship


from .base_model import Base
from .enums import LocationTag


class Tile(Base):
    __tablename__ = 'apeiros_location_tiles'

    id: Mapped[int] = mapped_column(primary_key=True)

    image = mapped_column(type_=BLOB)


# class Card(Base):
#     __tablename__ = 'apeiros_location_cards'

#     id: Mapped[int] = mapped_column(primary_key=True)

#     image = mapped_column(type_=BLOB)


class Location(Base):
    __tablename__ = 'apeiros_locations'

    # There can only be one location per coordinate, so they are the primary keys
    x: Mapped[int] = mapped_column(primary_key=True)
    y: Mapped[int] = mapped_column(primary_key=True)

    # Details
    name: Mapped[str]
    description: Mapped[str]

    # Png byte blobs
    tile_id: Mapped[int] = mapped_column(ForeignKey('apeiros_location_tiles.id'))
    tile_image: Mapped[Tile] = relationship()

    # card_id: Mapped[int] = mapped_column(ForeignKey('apeiros_location_cards.id'))
    # card_image: Mapped[Card] = relationship()

    # Proposal Details
    tile_submitter_id: Mapped[int] = mapped_column(ForeignKey('apeiros_players.id'))
    tile_submitter = relationship('Player', foreign_keys=tile_submitter_id)

    submission_fulfiller_id: Mapped[int] = mapped_column(ForeignKey('apeiros_players.id'))
    submission_fulfiller = relationship('Player', foreign_keys=submission_fulfiller_id)

    # Terrain tags, stored as a comma-separated string
    _tags: Mapped[str] = mapped_column('tags', default='')

    # Constructor for unpacking _tags once loaded
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._tag_list: List[LocationTag] = []
        self._unpack_tags()

    def _unpack_tags(self) -> List[str]:
        if self._tags is None or self._tags == '':
            self._tag_list = []
            return []

        tag_strings = self._tags.split(',')
        self._tag_list = [LocationTag[s] for s in tag_strings]

        return tag_strings

    def _pack_tags(self) -> None:
        self._tags = ','.join(self._tag_list)

    def add_tag(self, tag: LocationTag) -> None:
        if tag not in self._tag_list:
            self._tag_list.append(tag)
            self._pack_tags()

    def remove_tag(self, tag: LocationTag) -> None:
        if tag in self._tag_list:
            self._tag_list.remove(tag)

    def has_tag(self, tag: LocationTag) -> bool:
        return tag in self._tag_list

    def get_tags(self) -> List[LocationTag]:
        return self._tag_list

    # Public Methods #
    def __repr__(self):
        return (f'Location(name={self.name!r}, details={self.details!r}, x={self.location_x}, y={self.location_y}, '
                f'tags={self._unpack_tags()!r})')


class LocationProposal(Base):
    '''Used for the image half of a location proposal.'''

    __tablename__ = 'apeiros_location_proposals'

    id: Mapped[int] = mapped_column(primary_key=True)

    tile_id: Mapped[int] = mapped_column(ForeignKey('apeiros_location_tiles.id'))
    tile_image: Mapped[Tile] = relationship()

    submitter_id: Mapped[int] = mapped_column(ForeignKey('apeiros_players.id'))
    submitter = relationship('Player')
