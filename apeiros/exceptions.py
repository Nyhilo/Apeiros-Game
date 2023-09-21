# Custom exceptions for Apeiros

# Player Exceptions #
class PlayerNotFound(Exception):
    pass


class BadMovementDirection(Exception):
    pass


class BadMovementDistance(Exception):
    pass


# Location Exceptions #

class LocationOverlapError(Exception):
    '''
    Thrown when the program attempts to save a location at a coordinate that
    already contains a location.
    '''
    pass