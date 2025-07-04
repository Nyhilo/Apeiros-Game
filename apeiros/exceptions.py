# Custom exceptions for Apeiros

# Player Exceptions #
class PlayerNotFound(Exception):
    pass


class BadMovementDirection(Exception):
    pass


class BadMovementDistance(Exception):
    pass


class PlayerNicknameTaken(Exception):
    pass


class PlayerAlreadyHasMedal(Exception):
    '''
    Thrown when giving a medal to a player that is already associated with them.
    '''
    pass


class PlayerDoesntHaveMedal(Exception):
    '''
    Thrown when removing a medal from a player that they do not have.
    '''
    pass


# Location Exceptions #
class LocationOverlapError(Exception):
    '''
    Thrown when the program attempts to save a location at a coordinate that
    already contains a location.
    '''
    pass


# Image Exceptions #
class ImageNotSquareError(Exception):
    '''
    Thrown when a given image does not fall within the configured squareness
    requirements.
    '''
    pass
