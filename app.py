import time
from threading import Thread

from PIL import ImageTk

from potentials.config import draw_fun, get_results_fun, get_min_range, potential

from gui import init

calc_filename = ''

e = 0.0001
radius_e = 0.4
k = 1
safe_radius = 10
n = 10
plot = None
potentials = None
safe_zones = None
show_plot_b = False
# TODO: система сохранения и октрытия вычесленных моделей


def callback():
    # TODO: уведомление при получении результате
    pass


def show_close_hook():
    global show_plot_b
    # TODO: просьба закрыть окно графика, если оно открыто

    show_plot_b = not show_plot_b


def draw(real_size):
    global potentials, safe_zones, safe_radius, plot
    try:
        # TODO: уведомление(подтверждение отрисовки) + проверка на наличие графика
        print('drawing')
        plot = draw_fun(potentials, real_size, safe_zones, safe_radius, n)
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


class Gui:
    # TODO: создать систему уведомлений
    def __init__(self, calc_hook, draw_hook):
        init(self)
        calc_args = [self.qs, self.size]
        draw_args = [self.size]
        self.calc_hook_btn.config(command=lambda: calc_hook(calc_args))
        self.draw_hook_btn.config(command=lambda: draw_hook(draw_args))
        self.show_close_hook_btn.config(command=show_close_hook)

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
while True:
    try:
        print(1)
        if show_plot_b:
            plot.show()
            show_plot_b = False

        time.sleep(1)
    except Exception as ex:
        print(ex)
# в круге крутиться проверка хуков нет, хук должен запускать функцию в отдельном потоке
# возврат проверяется в кругу
