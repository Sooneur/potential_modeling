import matplotlib.pyplot as plot
from matplotlib import cm
import numpy as np


def new_draw(potentials: list, real_size: tuple, safe_zones: list, safe_radius: int, n: int):
    # TODO: width и height + доп параметры для просмотра отдельной части графика
    width, height = real_size
    width_m, height_m = real_size
    max_p = 0
    min_p = 0
    values = []
    contours = []
    for y in range(height_m):
        for x in range(width_m):
            if potentials[y][x] not in ('+', '-'):
                if min_p > float(potentials[y][x]):
                    min_p = float(potentials[y][x])
                if max_p < float(potentials[y][x]):
                    max_p = float(potentials[y][x])
    # TODO: Переписать на максимумах и минимумах
    for y in range(height_m):
        for x in range(width_m):

            if safe_zones[y][x] == 0:
                if potentials[y][x] == '+':
                    potentials[y][x] = max_p
                elif potentials[y][x] == '-':
                    potentials[y][x] = min_p
                continue

            if safe_zones[y][x] <= safe_radius:
                if float(potentials[y][x]) > 0:
                    potentials[y][x] = max_p
                else:
                    potentials[y][x] = min_p
                continue

            values.append(float(potentials[y][x]))
            potentials[y][x] = float(potentials[y][x])

    max_v, min_v = max(values), min(values)
    step = (max_v - min_v) / n
    for i in range(n):
        contours.append(step * i + min_v)


    X = np.arange(0, width, 1)
    Y = np.arange(0, height, 1)
    potentials = np.array(potentials)
    print(1)
    Z = potentials[Y][X]
    X, Y = np.meshgrid(X, Y)

    fig, ax = plot.subplots(subplot_kw={"projection": "3d"},)

    # ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
    ax.contour(X, Y, Z, contours, cmap=cm.coolwarm, alpha=1)

    ax.set(xlim=(width * 0 + int(width * 0.0) + 25, width + int(width * -0.0) + 50),
           ylim=(height * 0 + int(height * 0.0), height + int(height * 0.0)))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Potential")
    return fig, ax
