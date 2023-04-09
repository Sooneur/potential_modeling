import time
import tkinter
from threading import Thread
import matplotlib.pyplot as plot
import numpy as np
from PIL import ImageTk
from matplotlib import cm
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from potentials.config import draw_fun, get_results_fun, get_min_range, potential

from gui import init

calc_filename = ''

e = 0.0001
radius_e = 0.4
k = 1
safe_radius = 10
n = 10
fig = None
ax = None
potentials = None
safe_zones = None
show_plot_b = False
# TODO: система сохранения и октрытия вычесленных моделей


def callback():
    # TODO: уведомление при получении результате
    pass


# def show_close_hook():
#     global plot
#     plot.show()


def draw(real_size):
    global potentials, safe_zones, safe_radius
    try:
        # TODO: уведомление(подтверждение отрисовки) + проверка на наличие графика
        print('drawing')
        fig, ax = draw_fun(potentials, real_size, safe_zones, safe_radius, n)
        print('drawn')
        callback()
    except Exception as ex:
        print(ex)


def calculate(qs: dict, size: tuple):
    global potentials, safe_zones, safe_radius
    if not qs:
        raise Exception
    print('calculating')
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
            potentials[y][x] = potential(qs, (x, y), safe_radius)
            # TODO: safe_zones как побочный продукт potentials
            safe_zones[y][x] = get_min_range(qs, (x, y))

    print('calculated')
    # TODO: отправка сообщений в круг
    callback()


class Hook:

    def __init__(self, target):
        self.target = target
        # self.break_e = break_e

    def run(self, args):
        self.thread = Thread(target=self.target, args=args)
        self.thread.start()


# def draw_plot():
#     global plot
#     plot.show()


class Gui:
    # TODO: создать систему уведомлений
    def __init__(self, calc_hook, draw_hook):
        init(self)
        calc_args = [self.qs, self.size]
        draw_args = [self.size]
        self.calc_hook_btn.config(command=lambda: calc_hook(calc_args))
        self.draw_hook_btn.config(command=lambda: draw_hook(draw_args))
        self.show_close_hook_btn.config(command=self.draw_plot)

    def get_q(self):
        return self.qs

    def add_q(self):
        # TODO: добавить обработку наличия входящей информации + валидацию + уведомления о неправильном вводе
        x, y, q = self.x_en.get().strip(), self.y_en.get().strip(), self.q_en.get().strip()
        if not x.isdigit() or not y.isdigit() or not q.isdigit():
            return
        x, y, q = int(x), int(y), int(q)
        if x not in range(self.im_w) or y not in range(self.im_h):
            return
        self.qs[(x, y)] = q
        self.change_q_list()
        self.redraw()

    def clear_q_list(self):
        for item in self.q_list.get_children():
            self.q_list.delete(item)

    def change_q_list(self):
        self.clear_q_list()
        for keys in sorted(self.qs.keys()):
            self.q_list.insert(parent='', index='end', text='',
                               values=(keys[0], keys[1], self.qs[keys]))

    def redraw(self):
        pixels = self.image.load()
        for key in self.qs.keys():
            if self.qs[key] > 0:
                pixels[key] = 255, 0, 0
            else:
                pixels[key] = 0, 0, 255

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

    def draw_plot(self):
        global potentials, safe_zones
        real_size = self.size
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
        Z = potentials[Y][X]
        X, Y = np.meshgrid(X, Y)

        fig, ax = plot.subplots(subplot_kw={"projection": "3d"}, )
        canvas = FigureCanvasTkAgg(fig, self.root)  # A tk.DrawingArea.
        canvas.draw()
        # ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
        ax.contour(X, Y, Z, contours, cmap=cm.coolwarm, alpha=1)

        ax.set(xlim=(width * 0 + int(width * 0.0) + 25, width + int(width * -0.0) + 50),
               ylim=(height * 0 + int(height * 0.0), height + int(height * 0.0)))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Potential")
        toolbar = NavigationToolbar2Tk(canvas)
        toolbar.update()
        canvas.get_tk_widget().pack()

    def resize(self):
        # TODO: сделать функцию
        pass

    def calc(self):
        return

    def run(self):
        self.root.mainloop()


def run_app():
    gui = Gui(
        Hook(calculate).run,
        Hook(draw).run
    )
    gui.run()


app = Thread(target=run_app)
app.start()

# в круге крутиться проверка хуков нет, хук должен запускать функцию в отдельном потоке
# возврат проверяется в кругу
