import time
from math import cos, pi, sin
from threading import Thread
from potentials.config import draw_fun, get_results_fun, calculate_fun, save_results_fun

need_to_calc_status = False
need_to_draw_status = False

def calc():
    global need_to_calc_status
    while True:
        if not need_to_calc_status:
            time.sleep(2)
        else:
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
                need_to_calc_status = False
            except Exception as ex:
                print(ex)


calculator = Thread(target=calc)

calculator.start()

while True:
    a = input()
    print(drawer.is_alive(), calculator.is_alive())
    if a == 'd':
        need_to_draw_status = True
    if a == 'c':
        need_to_calc_status = True
    if not drawer.is_alive() or not calculator.is_alive():
        break
