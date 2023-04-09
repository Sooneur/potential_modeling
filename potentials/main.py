from math import cos, sin, pi
from random import randint, uniform
from config import draw_fun, calculate_fun, save_results_fun, get_results_fun

safe_radius = 2
n = 25


e = 0.0001
radius_e = 0.4
k = 9 * 10 ** 5
real_size = real_width, real_height = 1000, 1000
real_to_pic = 1
calc = False


def cic(r, x0, y0, qs):
    for fi in range(360):
        qs[x0 + r * cos(fi / 180 * pi), y0 + r * sin(fi / 180 * pi)] = 1

    return qs


def main(filename):
    pic_size = pic_width, pic_height = round(real_width * real_to_pic), round(real_height * real_to_pic)
    if calc:
        qs = {}
        qs = cic(10, real_width / 2, real_width / 2, qs)
        # for i in range(10):
        #     qs[randint(0, int(real_width * 0.25)),
        #        randint(0, int(real_height * 0.25))] = uniform(-1000, 1000)  # randint(1, 100) / 100
        # for fi in range(360):
        #     qs[real_width / 2 + 100 * cos(fi / 180 * pi), real_height / 2 + sin(fi / 180 * pi)] = 1
        # for i in range(100):
        #     qs[real_width / 2 + 25, i + real_height / 4] = 1
        #     qs[real_width / 2, i + real_height / 4] = -1
        # qs[50, 50] = 1
        # qs[150, 150] = -1
        # qs[600, 600] = 1

        results = calculate_fun(qs, real_size, radius_e, k)
        save_results_fun('modules/calc/' + filename, results)
    else:
        results = get_results_fun('modules/calc/' + filename)
        res, safe_zones = results
        # image = draw_fun(res, pic_size, real_to_pic, safe_zones, safe_radius, n, e)
        plot = draw_fun(res, pic_size, real_to_pic, safe_zones, safe_radius, n, e)
        plot.show()
        # image.save('modules/results/' + filename)

    # image.show()
    # save_image(image)


if __name__ == '__main__':
    main('0')
# 0 1 2 3 4 5 6 5
