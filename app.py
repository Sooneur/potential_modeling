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
calculate_b = False
draw_plot_b = False
callback_b = False


def callback():
    callback_b = True


def calculate(qs: dict, size: tuple):
    global potentials, safe_zones, safe_radius
    if not qs:
        raise Exception
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

    def __init__(self, calc_hook):
        init(self)
        args = [self.qs, self.size]
        self.calc_hook_btn.config(command=lambda: calc_hook(args))

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


def draw():
    global safe_radius
    try:
        print('drawing')
        results = get_results_fun('potentials/modules/calc/' + calc_filename)
        res, safe_zones = results
        real_size = len(res[0]), len(res)

        new_plt = draw_fun(res, real_size, safe_zones, safe_radius, n)
        # callback_draw(new_plt)
    except Exception as ex:
        print(ex)


def run_app():
    gui = Gui(Hook(calculate).run)
    gui.run()


def loop():
    # TODO: перехват сообщений и отправка уведомлений в gui
    while True:
        if callback_b and not ():
            callback_b = False
            pass

        time.sleep(0.1)

    pass


main_loop = Thread(target=loop)
app = Thread(target=run_app)
app.start()
app.join()

# в круге крутиться проверка хуков нет, хук должен запускать функцию в отдельном потоке
# возврат проверяется в кругу
