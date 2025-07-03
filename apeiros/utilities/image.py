# Contains utilities for converting and checking the properties of images.

from io import BytesIO
from math import floor, ceil
from typing import Tuple

from PIL import Image


IMAGE_FORMAT = 'PNG'


def check_square(image: bytes) -> Tuple[int, int, int, int]:
    '''
    Checks how square the image is. Returns a tuple indicating how many pixels
     the image is off from being square, the percentage of the difference from
     the short-side of the image, and the given width and height of the image.
     For instance, an image of size 200x210 would report return
     (pixels, percent, width, height) = (10, 5, 200, 210).

    Args:
        image (bytes): An image byte-input. Should be a png formatted image.
                        Use convert_png if not

    Returns:
        (int, int): (pixels_off, percent_off). Values indicating how far the
                     image is from being square.
    '''
    img = Image.open(BytesIO(image))

    width, height = img.size
    diff = abs(width - height)
    percent = 0 if diff == 0 else int((diff / min(width, height)) * 100)
    return diff, percent, width, height


# TODO: Consider supporting/using WebP instead
def convert_png(image: bytes) -> bytes:
    '''
    Converts an image from a format supported by PIL (jpg, etc.) to a png.

    Args:
        image (bytes): An image of a format supported by PIL.

    Returns:
        bytes: A png encoded to bytes in memory.
    '''
    img = Image.open(BytesIO(image))

    if img.format == IMAGE_FORMAT:
        return image

    return _save_image_to_memory(img)


def autocrop(image: bytes) -> bytes:
    '''
    Crops the long side of an image to be the same length as the short side of
    the image.

    Args:
        image (bytes): Byte reprensentation of an image.

    Returns:
        bytes: cropped byte representation of an image.
    '''
    img = Image.open(BytesIO(image))

    width, height = img.size

    if width == height:
        return image

    short_len = min(width, height)

    # v_crop or h_crop will be 0 if it *is* the short side
    v_crop = height - short_len
    h_crop = width - short_len

    # top, bottom, left, and right
    top = floor(v_crop / 2)
    bottom = (height - ceil(v_crop / 2))
    left = floor(h_crop / 2)
    right = (width - ceil(h_crop / 2))

    cropped = img.crop((left, top, right, bottom))

    return _save_image_to_memory(cropped)


def _save_image_to_memory(image: Image) -> bytes:
    with BytesIO() as output:
        image.save(output, IMAGE_FORMAT)

        return output.getvalue()
