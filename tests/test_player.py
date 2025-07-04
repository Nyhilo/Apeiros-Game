import pytest

from PIL import UnidentifiedImageError

from apeiros import setup_database, create_player, get_player, check_square, \
    convert_png, autocrop, create_location, create_location_proposal
from apeiros.exceptions import LocationOverlapError


def printn(m):
    print('\n' + m)


# setup_database('sqlite:///db.sqlite3')
setup_database()


def test_convertPng_ConvertsToPng():
    with open('tests/test_imgs/test.jpg', 'rb') as f:
        png = f.read()

    _ = convert_png(png)

    with open('tests/test_imgs/location.webp', 'rb') as f:
        webp = f.read()

    _ = convert_png(webp)


def test_convertPng_textFileFails():
    with open('tests/test_imgs/test.txt', 'rb') as f:
        txt = f.read()

    with pytest.raises(UnidentifiedImageError):
        _ = convert_png(txt)


def test_cropImageSquare():
    with open('tests/test_imgs/test.jpg', 'rb') as f:
        data = f.read()

    image = convert_png(data)

    pixels, percent, _, _ = check_square(image)

    assert pixels == 1
    assert percent == 1

    cropped_image = autocrop(image)

    pixels, percent, _, _ = check_square(cropped_image)

    assert pixels == 0
    assert percent == 0


def test_createAndRetreivePlayers():
    with open('tests/test_imgs/test.jpg', 'rb') as f:
        data = f.read()

    player_image = autocrop(convert_png(data))

    id = 1
    create_player(str(id), 'playerA', 'playerA_nickname', player_image)
    assert get_player(str(id)).name == 'playerA_nickname'

    id += 1
    create_player(str(id), 'playerB_username', None, player_image)
    assert get_player(str(id)).name == 'playerB_username'

    id += 1
    create_player(str(id), None, 'playerC_nickname', player_image)
    assert get_player(str(id)).name == 'playerC_nickname'

    create_player(None, 'playerD_username', 'playerD_nickname', player_image)
    assert get_player('playerD_username').name == 'playerD_nickname'

    create_player(None, 'playerE_username', None, player_image)
    assert get_player('playerE_username').name == 'playerE_username'


def test_canChangePlayerNickname():
    with open('tests/test_imgs/test.jpg', 'rb') as f:
        data = f.read()

    player_image = autocrop(convert_png(data))
    player = create_player(None, 'player_username', 'player_nickname', player_image)

    player.nickname = 'player_newNickname'

    assert player.username == 'player_username'
    assert player.nickname == 'player_newNickname'
    assert player.name == 'player_newNickname'
    assert player.nickname != 'player_nickname'


def test_createdPlayerHasTimestamp():
    from datetime import datetime

    with open('tests/test_imgs/test.jpg', 'rb') as f:
        data = f.read()

    player_image = autocrop(convert_png(data))
    player = create_player(None, 'player', None, player_image)

    assert isinstance(player.created_at, datetime)


def test_locationOverlapRaisesError():
    with open('tests/test_imgs/test.jpg', 'rb') as f:
        data = f.read()

    player_image = autocrop(convert_png(data))
    player_a = create_player(None, 'player_a', None, player_image)
    player_b = create_player(None, 'player_b', None, player_image)
    player_c = create_player(None, 'player_c', None, player_image)

    with open('tests/test_imgs/location.webp', 'rb') as f:
        webp = f.read()

    location_image = autocrop(convert_png(webp))

    with pytest.raises(LocationOverlapError):
        proposal = create_location_proposal(player_a, location_image)
        create_location(0, 0, 'Location A', 'description', proposal, player_b)
        create_location(0, 0, 'Location B', 'description', proposal, player_c)
