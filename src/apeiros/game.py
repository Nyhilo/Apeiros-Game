from .database import Database

# Default database connection string is an in-memory sqlite db
_connectionString: str = 'sqlite+pysqlite:///:memory:'

# The database must be setup explicitly before anything else can take place
_db = None


def setup_database(connectionString: str = None) -> None:
    '''
    Takes a SqlAlchemy connection string. Default's to in-memory sqlite if None is given.

    Args:
        connectionString (str, optional): SqlAlchemy connection string. Defaults to None.
    '''
    global _connectionString
    global _db

    if connectionString is not None:
        _connectionString = connectionString

    _db = Database(_connectionString)


def db() -> Database:
    return _db
