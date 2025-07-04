from .game import db
from .models import Player, Location, Tile, LocationProposal
from .utilities import image
from .exceptions import ImageNotSquareError, LocationOverlapError
from .config import squareness_percent_off_limit


def create_location_proposal(
        submitter: Player,
        tile_image: bytes
) -> LocationProposal:
    '''
    Create a new proposal for a location. Checks for image squareness before accepting

    Args:
        submitter (Player): _description_
        tile_image (bytes): _description_

    Returns:
        LocationProposal: _description_
    '''

    pixels_off, percent_off, w, h = image.check_square(tile_image)
    if percent_off > squareness_percent_off_limit:
        crop_direction = 'sides' if w > h else 'top/bottom'
        raise ImageNotSquareError(f'Image is not square enough! We would need to crop {pixels_off} pixels off the '
                                  f'{crop_direction} of the image in order to make it square. Please resize it and try '
                                  'again')

    return LocationProposal(tile_image=Tile(image=tile_image), submitter=submitter)


def create_location(
    x: int,
    y: int,
    name: str,
    description: str,
    proposed_location: LocationProposal,
    proposal_fulfiller: Player
) -> Location:
    '''
    Create a new location. A location is formed when a Location Proposal -
    created by player and containing an image - if fulfilled by another player.

    Args:
        x (int):
            The x coordinate on the map. May be positive or negative
        y (int):
            The x coordinate on the map. May be positive or negative
        name (str):
            The name of the location.
        description (str):
            The description of the location.
        proposed_location (LocationProposal):
            The proposed tile for the location. Contains the player who proposed
            the location and the image for the tile.
        proposal_fulfiller (Player):
            The player who fulfilled the proposal. This is the player that
            offered the coordinates and descriptive information for this method.

    Raises:
        LocationOverlapError:
            Raises when a location already exists at the given coordinates

    Returns:
        Location:
            The location created
    '''

    # Check if a location already exists
    existing = db().get_location(x, y)
    if existing is not None:
        raise LocationOverlapError(f'Cannot create location. A location already exists at the coordinates ({x}, {y})')

    location = Location(
        x=x,
        y=y,
        name=name,
        description=description,
        tile_image=proposed_location.tile_image,
        tile_submitter=proposed_location.submitter,
        submission_fulfiller=proposal_fulfiller
    )

    db().add_location(location)

    return db().get_location(x, y)
