# Note that the values in this model are not saved to repository.
# It is kept here for hierarchy consistency

from enum import Enum


class NomsterType(str, Enum):

    # NOTE: If a member gets added to this list, also add it to the LocationTags enum below

    Heat = 'Heat'
    Electricity = 'Electricity'
    Plant = 'Plant'
    Air = 'Air'
    Light = 'Light'
    Cold = 'Cold'
    Water = 'Water'
    Metal = 'Metal'
    Land = 'Land'
    Dark = 'Dark'


class NomsterClass(str, Enum):
    Amphibian = 'Amphibian'
    Arthropoid = 'Arthropoid'
    Avian = 'Avian'
    Piscine = 'Piscine'
    Mammalian = 'Mammalian'
    Reptilian = 'Reptilian'


class LocationTag(str, Enum):
    # We continue to use strings here instead of a potentially more rational
    # bit-enum so that it will be easier to interrogate on the database. We
    # aren't going to be storing a very large number of tiles, so we aren't
    # concerned about wasting some data space on redundancy

    # The set of elemental types should always be the same as the set of nomster types
    Heat = NomsterType.Heat
    Electricity = NomsterType.Electricity
    Plant = NomsterType.Plant
    Air = NomsterType.Air
    Light = NomsterType.Light
    Cold = NomsterType.Cold
    Water = NomsterType.Water
    Metal = NomsterType.Metal
    Land = NomsterType.Land
    Dark = NomsterType.Dark

    # Development state of the tile. A location will typically not have both of these at the same time
    Wild = 'Wild'
    Populated = 'Populated'

    # Further development states for populated tiles
    Hospitable = 'Hospitable'
    Buildable = 'Buildable'
    Farm = 'Farm'
    Civilized = 'Civilized'


class Direction(Enum):
    North = 1,
    East = 2,
    South = 3,
    West = 4
