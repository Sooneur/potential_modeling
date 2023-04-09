from .get_min_range import get_min_range
from .potential import potential


def calculate(qs: dict, size: tuple, radius_e: float):
    if not qs:
        raise
    width, height = size
    potentials = [([0] * width) for _ in range(height)]
    safe_zones = [([0] * width) for _ in range(height)]

    cords = qs.keys()

    for x in range(width):
        for y in range(height):

            if (x, y) in cords:
                if qs[x, y] > 0:
                    potentials[y][x] = "+"
                else:
                    potentials[y][x] = "-"
                safe_zones[y][x] = 0
                continue
            potentials[y][x] = potential(qs, (x, y), radius_e)
            # TODO: safe_zones как побочный продукт potentials
            safe_zones[y][x] = get_min_range(qs, (x, y))

    return potentials, safe_zones
