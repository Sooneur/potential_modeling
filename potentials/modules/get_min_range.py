def get_min_range(dots: dict, point_cords: tuple) -> int:
    """
    Рассчитывает минимальное расстояние от одной до нескольких точек
    :param dots: dict of (x, y)
    :param point_cords: (x, y)
    :return: min_range: Минимальное расстояние
    """
    ranges = []
    for cord in dots.keys():
        x, y = point_cords
        xq, yq = cord

        r = ((x - xq) ** 2 + (y - yq) ** 2) ** 0.5
        ranges.append(r)
    return min(ranges)
