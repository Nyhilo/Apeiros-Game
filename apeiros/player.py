from typing import Tuple

from .game import db
from .models import Player, Medal, Item
from .models.enums import Direction
from .exceptions import PlayerNotFound, PlayerNicknameTaken, BadMovementDirection, BadMovementDistance, \
                        PlayerAlreadyHasMedal, PlayerDoesntHaveMedal
from .utilities import image


NORTH = {Direction.North, 1, 'north', 'n', 'up', 'u'}
EAST = {Direction.East, 2, 'east', 'e', 'right', 'r'}
SOUTH = {Direction.South, 3, 'south', 's', 'down', 'd'}
WEST = {Direction.West, 4, 'west', 'w', 'left', 'l'}
VALID_MOVEMENT_DIRECTIONS = NORTH.union(EAST).union(SOUTH).union(WEST)


def create_player(
        unique_id: str | None,
        username: str | None,
        nickname: str | None,
        player_token: bytes,
        autocrop: bool = False
) -> Player:
    '''
    !! Use check_square() before submitting an image through this method. !!

    Create a new player in the database. unique_id, username, and nickname may
    be None, with some restrictions:

    Both a unique_id and username MAY be given (and SHOULD be if available),
    but one OR the other MUST be given.

    If a unique_id is given but a username is not, then a nickname MUST be.

    All values not specified MUST be given as None, for clarity.

    Args:
        unique_id (str | None):
            A unique internal ID, such as a discord User ID
        username (str | None):
            A unique username. Will be displayed when clarity between useres is
            desired.
        nickname (str | None):
            A nickname. Takes precedence over username for identifying the user.
        player_token (bytes):
            A square png. Maximum size of 200kb.
        autocrop (bool):
            Indicates whether the player token should be automatically cropped
            to a square aspect ratio.

    '''
    # Sanitize identifiers
    unique_id, username, nickname = _handle_user_identifiers(unique_id, username, nickname)

    # Sanitize player token image
    player_token = _handle_player_token(player_token, autocrop)

    player = Player(
        unique_id=unique_id,
        username=username,
        nickname=nickname,
        player_token=player_token,
        points=0,
        medals=[],
        inventory=[],
        nomsters=[]
    )
    db().add_player(player)

    return player


def get_player(unique_id: str) -> str:
    '''
    Gets a player, if they exist.

    Raises:
        PlayerNotFound: Player doesn't exist

    Args:
        unique_id (str): The unique id of a player object. This value is
                            usually an arbitrary id set by the calling client,
                            but may be a username is another id was not
                            provided.

    Returns:
        str: The human-readable identifying string of the player.
    '''
    player = db().get_player(unique_id)

    if player is None:
        raise PlayerNotFound('No player found with that unique id.')

    return player


def move_player(player: Player, direction: Direction | str | int, distance: int = 1) -> None:
    '''
    Tries to move the player a certain number of squares in a gven direction.
    Accepts the following directions:
    North, East, South, West from apeiros.Direction.
    The strings "North", "East", "South", or "West".
    The strings "N", "E", "S", or "W".
    The strings "Up", "Right", "Down", or "Left".
    The integers 1, 2, 3, or 4, corresponding to the directions N, E, S, and W.
    All strings are non-case-sensitive.

    Args:
        direction (Direction | str | int): The direction to move.
    '''
    # Validate the direction is a correct form
    if type(direction) is str:
        direction = direction.lower()

    if direction not in VALID_MOVEMENT_DIRECTIONS:
        raise BadMovementDirection(f'The given direction "{direction}" is not a valid movement direction.')

    # Is our distance good?
    if distance < 0:
        raise ValueError('The distance to move must be greater than 1.')

    # Convert input to vector
    x, y = _normalize_direction(direction, distance)

    # Because we only move in a straight line right now, one of these values
    # will always stay the same (x or y will be 0)
    dest_x, dest_y = player.x + x, player.y + y

    # Check for blank locations along the x axis
    for _x in range(dest_x, player.x, 1 if player.x > dest_x else -1):
        if db().get_location(_x, player.y) is None:
            raise BadMovementDistance("You can't move like that. There is an undiscovered location that way.")

    # Check for blank locations along the y axis
    for _y in range(dest_x, player.x, 1 if player.x > dest_x else -1):
        if db().get_location(player.x, _y) is None:
            raise BadMovementDistance("You can't move like that. There is an undiscovered location that way.")

    # Teleport the player (nothing personal, kid)
    player.x = dest_x
    player.y = dest_y


def update_name(player: Player, nickname: str) -> None:
    '''
    Sets the nickname of the given player. Two players cannot share the same
    nickname, insensitive to case.

    Args:
        player (Player): The Player object to update.
        nickname (str): The new player nickname.

    Raises:
        PlayerNicknameTaken: Player nickname already taken by another player.
    '''
    existing = db().get_player_list()
    existing_nicknames = [p.nickname.lower() for p in existing]

    if nickname.lower() in existing_nicknames:
        raise PlayerNicknameTaken

    player.nickname = nickname

    db().update_player(player)


def update_token(player: Player, image: bytes, autocrop: bool = False) -> None:
    '''
    Updates the token for the given player. The given image should be square.

    Args:
        player (Player): The Player object to update.
        image (bytes): The image to set as the player token.
        autocrop (bool, optional): If true, the image will be cropped square. Defaults to False.
    '''
    player_token = _handle_player_token(image, autocrop)

    player.player_token = player_token

    db().update_player(player)


def add_medal(player: Player, medal: Medal) -> None:
    '''
    Give a medal to the specified player.

    Args:
        player (Player): The Player object to update.
        medal (Medal): The Medal object to associate with the player.

    Raises:
        PlayerAlreadyHasMedal: Player already has the given medal.
    '''
    if medal.medal_id in [m.medal_id for m in player.medals]:
        raise PlayerAlreadyHasMedal

    player.medals.add(medal)

    db().update_player(player)


def remove_medal(player: Player, medal: Medal) -> None:
    '''
    Removes a medal from the specified player.

    Args:
        player (Player): The Player object to update.
        medal (Medal): The Medal object to remove from the player.

    Raises:
        PlayerDoesntHaveMedal: Player doesn't have the specified medal.
    '''
    if medal.medal_id not in [m.medal_id for m in player.medals]:
        raise PlayerDoesntHaveMedal

    player.medals.remove(medal)

    db().update_player(player)


def add_item(player: Player, item: Item, amount: int = 1) -> None:
    '''
    Give an item to the specified player.

    Args:
        player (Player): The Player object to update.
        item (Item): The Item object to add to the player's inventory.
        amount (int, optional): The quantity of the item to add. Defaults to 1.
    '''
    player.add_item(item)


def remove_item(player: Player, item: Item, amount: int = 1) -> int:
    '''
    Remove an item from the specified player.

    Args:
        player (Player): The Player object to update.
        item (Item): The Item object to remove from the player's inventory.
        amount (int, optional): The quantity of the item to remove. Defaults to 1.

    Returns:
        int: The amount of items removed
    '''
    slot = player.get_slot(item.item_id)

    if slot is None:
        return 0

    amount = min(slot.amount, amount)

    player.remove_item(item, amount)


#####################
# Utility Functions #
#####################

# Written with Lily's help :)
def _handle_user_identifiers(unique_id: str, username: str, nickname: str) -> Tuple[str, str, str]:
    has_unique_id = unique_id is not None
    has_username = username is not None
    has_nickname = nickname is not None

    match (has_unique_id, has_username, has_nickname):
        case (False, False, False):
            raise ValueError('Bro you didn\'t even give any ids. Why do you think those params are there?')
        case (_, False, False):
            raise ValueError('If a username is not given, a nickname must be provided to identify the player.')
        case (False, False, _):
            raise ValueError('Either a unique_id or a username must be given to create a new player.')
        case (False, True, _):
            unique_id = username
        case (_, True, False):
            nickname = username

    return (unique_id, username, nickname)


def _handle_player_token(token: bytes, autocrop: bool = False) -> bytes:
    # We'll just convert the image just to make sure
    token = image.convert_png(token)

    pixels_off, _, _, _ = image.check_square(token)
    if pixels_off > 0 and not autocrop:
        raise ValueError('Given player token image is not square.')

    if autocrop:
        return image.autocrop(token)

    return token


def _normalize_direction(direction: Direction | str | int, distance: int) -> Tuple[int, int]:
    '''
    Converts a direction and a distance to a movement vector (x, y).
    For example, a direction of "west" and a distance of 3 would result in the
    vector (-3, 0)
    '''
    x, y = (0, 0)

    if direction in NORTH or direction in SOUTH:
        y = distance
    else:   # East or West
        x = distance

    if direction in EAST or direction in SOUTH:
        x, y = -x, -y

    return (x, y)
