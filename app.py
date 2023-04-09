from time import sleep

from math import cos, pi, sin
from threading import Thread
from potentials.config import draw_fun, get_results_fun, calculate_fun, save_results_fun


calc_filename = '0.txt'

e = 0.0001
radius_e = 0.4
k = 9 * 10 ** 9
real_size = real_width, real_height = 1000, 1000
real_to_pic = 1
safe_radius = 10
n = 10

plot = None
show_plot = False


def calc():
    try:
        print('calculating')
        qs = {}
        # for i in range(10):
        #     qs[randint(0, real_width),
        #        randint(0, real_height)] = uniform(-1000, 1000)  # randint(1, 100) / 100
        for fi in range(360):
            qs[real_width / 2 + 100 * cos(fi / 180 * pi), real_height / 2 + 100 * sin(fi / 180 * pi)] = 1
        # qs[50, 50] = 1
        # qs[150, 150] = -1
        # qs[600, 600] = 1

        results = calculate_fun(qs, real_size, radius_e, k)
        save_results_fun('potentials/modules/calc/' + calc_filename, results)

        print('calculated')
    except Exception as ex:
        print(ex)


def callback_show_plot():
    global show_plot
    print('callback_show')
    show_plt = True


def callback_draw(new_plot):
    global plot
    plot = new_plot


def draw():
    global safe_radius
    try:
        print('drawing')
        results = get_results_fun('potentials/modules/calc/' + calc_filename)
        res, safe_zones = results
        pic_size = len(res[0]), len(res)

        # image = draw_fun(res, pic_size, real_to_pic, safe_zones, safe_radius, n, e)
        new_plt = draw_fun(res, pic_size, real_to_pic, safe_zones, safe_radius, n, e)
        callback_draw(new_plt)
    except Exception as ex:
        print(ex)


def loop():
    global show_plot
    while True:
        sleep(3)
        if show_plot:
            show_plot = False


calculator = Thread(target=calc)
drawer = Thread(target=draw)
loop = Thread(target=loop)
# Todo: заменить qt а tkinter



