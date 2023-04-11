import tkinter
from threading import Thread, Event
import matplotlib.pyplot as plot
import numpy as np
from PIL import ImageTk
from matplotlib import cm
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from potentials.config import get_min_range, potential

from gui import init

safe_radius = 10
n = 20
threads = {}
fig = None
ax = None
event = Event()
potentials = None
safe_zones = None
d_cords = None


# TODO: система сохранения и октрытия вычесленных моделей
# TODO: система импорта картинки
# TODO: отображение степени отрисовки(прогресс бар)


def callback():
    # TODO: уведомление при получении результате
    pass


def draw(real_size):
    global potentials, safe_zones, safe_radius, d_cords
    try:
        # TODO: уведомление(подтверждение отрисовки) + проверка на наличие графика
        print('drawing')
        # TODO: width и height + доп параметры для просмотра отдельной части графика
        width, height = real_size
        width_m, height_m = real_size
        max_p = 0
        min_p = 0
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

                potentials[y][x] = float(potentials[y][x])

        step = (max_p - min_p) / n
        for i in range(n):
            contours.append(step * i + min_p)

        X = np.arange(0, width, 1)
        Y = np.arange(0, height, 1)
        potentials = np.array(potentials)
        Z = potentials[Y][X]
        X, Y = np.meshgrid(X, Y)

        d_cords = X, Y, Z, contours
        callback()
        print('drawn')
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


# TODO: поправить отрисовку графика или сделать смену угла обзора(выбора)
class PlotWindow:
    def __init__(self, main_window):
        self.root = tkinter.Toplevel(main_window.root)
        # TODO: специальное имя для каждого графика???(нужно ли)
        self.root.title('Plot')
        self.size = main_window.size
        self.qs = main_window.qs
        self.calc_hook = main_window.calc_hook
        self.draw_hook = main_window.draw_hook

    def draw_plot(self):
        global potentials, safe_zones, d_cords
        # TODO: проверка на наличие графика(работает ли)
        everything_done = True
        if potentials is None or safe_zones is None:
            everything_done = False
            callback()
        if d_cords is None:
            everything_done = False
            callback()
        if not everything_done:
            try:
                self.root.destroy()
            except Exception as ex:
                print(ex)
            return
        # # TODO: width и height + доп параметры для просмотра отдельной части графика
        width, height = self.size
        X, Y, Z, contours = d_cords
        #
        figure, axis = plot.subplots(subplot_kw={"projection": "3d"}, )
        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.draw()

        axis.contour(X, Y, Z, contours, cmap=cm.coolwarm, alpha=1)

        axis.set(xlim=(0, width), ylim=(0, height))
        axis.set_xlabel("X")
        axis.set_ylabel("Y")
        axis.set_zlabel("Potential")
        toolbar = NavigationToolbar2Tk(canvas)
        toolbar.update()
        canvas.get_tk_widget().pack()


# TODO: добавить немного дизайна(кнопки нормально расставь!!!)
# TODO: добавить время от последних вычислений
class MainWindow:
    # TODO: создать систему уведомлений
    def __init__(self, calc_hook, draw_hook):
        init(self)
        self.calc_hook = calc_hook
        self.draw_hook = draw_hook
        self.calc_hook_btn.config(command=lambda: calc_hook.run([self.qs, self.size]))
        self.draw_hook_btn.config(command=lambda: draw_hook.run([self.size]))
        self.show_hook_btn.config(command=self.draw_plot)

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
        for q_key in self.qs.keys():
            if self.qs[q_key] > 0:
                pixels[q_key] = 255, 0, 0
            else:
                pixels[q_key] = 0, 0, 255

        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

    def draw_plot(self):
        new_plot_window = PlotWindow(self)
        new_plot_window.draw_plot()

    def resize(self):
        # TODO: сделать функцию смены размеров графика
        pass

    def calc(self):
        return

    def run(self):
        self.root.mainloop()


class Hook:

    def __init__(self, target):
        self.target = target
        # self.break_e = break_e

    def run(self, args):
        global threads
        self.thread = Thread(target=self.target, args=args)
        self.thread.start()
        threads[self] = self.thread


gui = MainWindow(
    Hook(calculate),
    Hook(draw)
)
gui.root.mainloop()
print(1)
for key in threads.keys():
    threads[key].join()
    print(key)
# в круге крутиться проверка хуков нет, хук должен запускать функцию в отдельном потоке
# возврат проверяется в кругу
