from typing import Optional

from sqlalchemy import ForeignKey, BLOB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from .enums import NomsterType, NomsterClass


class Species(Base):
    '''A limited table of Nomster species. These start out unnammed, and gain names once discovered.'''

    __tablename__ = 'apeiros_species'

    id: Mapped[int] = mapped_column(primary_key=True)

    # Player-defined details
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    # 'Class' and 'Type' are keywords :)
    nomster_type: Mapped[NomsterType]
    nomster_class: Mapped[NomsterClass]

    # PNG byte BLOB
    portrait = mapped_column(type_=BLOB, nullable=True)

    def __repr__(self):
        return (f'Species(type={self.nomster_type.value!r}, class={self.nomster_class.value!r}, '
                f'species={self.name!r}, description={self.description!r})')


class Nomster(Base):
    __tablename__ = 'apeiros_nomsters'

    id: Mapped[int] = mapped_column(primary_key=True)

    # What kind of nomster is this anyway?
    species_id: Mapped[int] = mapped_column(ForeignKey('apeiros_species.id'))
    species: Mapped['Species'] = relationship()

    location_x: Mapped[int]
    location_y: Mapped[int]

    # Tamed attributes #
    # Everything under this is optional if this value is False
    is_tamed: Mapped[bool] = mapped_column(insert_default=False)

    name: Mapped[Optional[str]]

    # Owner and orignal owner foreign key relationships
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('apeiros_players.id'))
    owner = relationship('Player', back_populates='nomsters', foreign_keys=owner_id)

    original_owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey('apeiros_players.id'))
    original_owner = relationship('Player', foreign_keys=original_owner_id)

    # Public Methods #
    def __repr__(self):
        ownerName = self.owner.nickname if self.owner is not None else None
        return (f'Nomster(species={self.species.name!r}, x={self.location_x}, y={self.location_y}, '
                f'tamed={self.is_tamed}, name={self.name!r}, owner={ownerName!r})')
