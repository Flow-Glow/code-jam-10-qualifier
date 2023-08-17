import numpy as np
from PIL import Image


def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    height = image_size[0] % tile_size[0]
    width = image_size[1] % tile_size[1]
    if (height != 0) or (width != 0):
        return False
    num_tiles = (image_size[0] // tile_size[0]) * (image_size[1] // tile_size[1])
    return (len(ordering) == num_tiles) and sorted(ordering) == list(range(num_tiles))


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering is not valid for the given image".
    """
    image = Image.open(image_path)
    if valid_input(image.size, tile_size, ordering):
        new_image = Image.new(image.mode, image.size)
        correct_ordering = np.argsort(ordering)
        for i in range(len(ordering)):
            x = i % (image.size[0] // tile_size[0])
            y = i // (image.size[0] // tile_size[0])
            tile = image.crop((x * tile_size[0], y * tile_size[1], (x + 1) * tile_size[0], (y + 1) * tile_size[1]))
            new_image.paste(tile, (correct_ordering[i] % (image.size[0] // tile_size[0]) * tile_size[0],
                                   correct_ordering[i] // (image.size[0] // tile_size[0]) * tile_size[1]))
        new_image.save(out_path)
        new_image.close()
        image.close()

    else:
        image.close()
        raise ValueError("The tile size or ordering are not valid for the given image")

