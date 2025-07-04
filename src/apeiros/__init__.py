'''
Apeiros. A game about discovering the world and making friends.

This file defines the public interface for the game.
'''

from .game import setup_database
from .player import (
    create_player,
    get_player
)
from .location import (
    create_location,
    create_location_proposal
)

from .exceptions import *
from .utilities.image import (
    check_square,
    convert_png,
    autocrop
)
