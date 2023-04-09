def potential(qs: dict, point_cords: tuple, radius_e: float, k: float):
    """Значение потенциала в точке"""
    cords = qs.keys()
    p_x, p_y = point_cords

    if abs(round(p_x) - p_x) < radius_e and \
            abs(round(p_y) - p_y) < radius_e:
        point_cords = round(p_x), round(p_y)
        # print(point_cords)

    f = 0
    for cord in cords:
        x, y = point_cords
        xq, yq = cord
        q = qs[cord]
        r = ((x - xq) ** 2 + (y - yq) ** 2) ** 0.5

        f += k * q / r

    return round(f, 5)
