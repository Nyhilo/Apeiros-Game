from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .models import Base, Player, Medal, Item, Species, Nomster, Location


class Database():
    '''Contains game database interface methods.'''
    def __init__(self, connectionString: str) -> None:
        if connectionString is None:
            raise RuntimeError('No connection string provided.')

        self.engine = create_engine(connectionString)
        Base.metadata.create_all(self.engine)

        self.session = Session(self.engine)

    # Players #
    def add_player(self, player: Player) -> None:
        self.session.add(player)

    def get_player(self, unique_id: str) -> Player:
        return self.session.scalar(select(Player).where(Player.unique_id == unique_id))

    def get_player_list(self, unique_ids: List[str] = None) -> List[Player]:
        if unique_ids is None:
            return self.session.scalars(select(Player)).all()

        elif type(unique_ids) is list:
            return self.session.scalars(select(Player).where(Player.unique_id.in_(unique_ids))).all()

    def update_player(self, player: Player) -> None:
        self.session.merge(player)

    # Medals #
    def upsert_medal(self, medal: Medal) -> None:
        self.session.merge(medal)

    def get_medal(self, medal_id: str) -> Medal:
        return self.session.get(Medal, medal_id)

    def get_medal_list(self):
        return self.session.scalars(select(Medal)).all()

    # Items #
    def upsert_item(self, item: Item) -> None:
        self.session.merge(item)

    def get_item(self, item_id: str) -> Item:
        return self.session.get(Item, item_id)

    def get_item_list(self) -> List[Item]:
        return self.session.scalars(select(Item)).all()

    # Nomster Species #
    def upsert_species(self, species: Species) -> None:
        self.session.merge(species)

    def get_species(self, species_id: int) -> Species:
        return self.session.get(Species, species_id)

    def get_species_list(self) -> List[Species]:
        return self.session.scalars(select(Species)).all()

    # TODO: Implement extra helper database methods
    # def get_species_by_type(self, type: NomsterType) -> Species
    # def get_species_list_by_location(self, x: int, y: int) -> List[Species]

    # Nomsters #
    def add_nomster(self, nomster: Nomster) -> None:
        self.session.add(nomster)

    def get_nomster(self, nomster_id: int) -> Nomster:
        self.session.get(Nomster, nomster_id)

    def get_player_nomsters(self, player: int | Player) -> List[Nomster]:
        player_id = player if type(player) is int else player.id

        return self.session.scalars(select(Nomster).where(Nomster.owner_id == player_id)).all()

    # Locations #
    def add_location(self, location: Location) -> None:
        if self.get_location(location.x, location.y) is not None:
            raise ValueError('A location already exists at that set of coordinates')

        self.session.add(location)

    def get_location(self, x: int, y: int) -> Location:
        return self.session.get(Location, (x, y))

    def get_location_list(self) -> List[Location]:
        return self.session.scalars(select(Location)).all()
