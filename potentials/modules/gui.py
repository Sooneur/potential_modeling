from threading import Thread
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk


class Gui:
    def __init__(self):
        self.qs = {}
        self.im_w, self.im_h = 600, 600
        self.image = Image.new('RGB', (self.im_w, self.im_h), 'white')
        # self.image = Image.open('0.png')
        self.root = tkinter.Tk()

        # Image
        self.image_frame = tkinter.Frame(self.root)
        self.image_frame.grid()

        # Canvas
        self.canvas = tkinter.Canvas(self.image_frame, height=600, width=600,
                                     scrollregion=(0, 0, self.im_w, self.im_h))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.grid()

        # Vertical bar
        self.vertibar = tkinter.Scrollbar(self.image_frame, orient=tkinter.VERTICAL)
        self.vertibar.grid(row=0, sticky='nse')
        self.vertibar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vertibar.set)

        # Horizontal bar
        self.horibar = tkinter.Scrollbar(self.image_frame, orient=tkinter.HORIZONTAL)
        self.horibar.grid(sticky='wes')
        self.horibar.config(command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.horibar.set)

        # Data Frame
        self.data_frame = tkinter.Frame(self.root)
        self.data_frame.grid(row=0, column=1)
        # Q managing
        self.q_managing_frame = tkinter.Frame(self.data_frame)
        self.q_managing_frame.grid(row=0, column=0)

        # Input Frame
        self.input_frame = tkinter.Frame(self.q_managing_frame)
        self.input_frame.grid(row=0, column=0)

        self.x_l = tkinter.Label(self.input_frame, width=10, text='x')
        self.x_l.grid(column=0, row=0)
        self.y_l = tkinter.Label(self.input_frame, width=10, text='y')
        self.y_l.grid(column=1, row=0)
        self.q_l = tkinter.Label(self.input_frame, width=10, text='q')
        self.q_l.grid(column=2, row=0)
        self.x_en = tkinter.Entry(self.input_frame, width=10)
        self.x_en.grid(column=0, row=1)
        self.y_en = tkinter.Entry(self.input_frame, width=10)
        self.y_en.grid(column=1, row=1)
        self.q_en = tkinter.Entry(self.input_frame, width=10)
        self.q_en.grid(column=2, row=1)
        self.add_btn = tkinter.Button(self.input_frame, text="Добавить",
                                      width=10, command=self.add_q)
        self.add_btn.grid(row=1, column=3)

        # List Frame
        self.list_frame = tkinter.Frame(self.q_managing_frame)
        self.list_frame.grid(row=1, column=0)

        self.q_list = ttk.Treeview(self.list_frame)
        self.q_list.grid(row=4, column=3)

        self.q_list['columns'] = ('x', 'y', 'q')
        cen = tkinter.CENTER
        self.q_list.column("#0", width=0, stretch=tkinter.NO)
        self.q_list.column("x", anchor=cen, width=80)
        self.q_list.column("y", anchor=cen, width=80)
        self.q_list.column("q", anchor=cen, width=80)

        self.q_list.heading("x", text="x", anchor=cen)
        self.q_list.heading("y", text="y", anchor=cen)
        self.q_list.heading("q", text="q", anchor=cen)

        # Resize Frame
        self.resize_frame = tkinter.Frame(self.data_frame)
        self.resize_frame.grid(row=1, column=0)

        self.w_l = tkinter.Label(self.resize_frame, width=10, text=f'width: {self.im_w}')
        self.w_l.grid(row=0, column=0)
        self.h_l = tkinter.Label(self.resize_frame, width=10, text=f'height: {self.im_h}')
        self.h_l.grid(row=0, column=1)
        self.w_en = tkinter.Entry(self.resize_frame, width=10)
        self.w_en.grid(row=1, column=0)
        self.h_en = tkinter.Entry(self.resize_frame, width=10)
        self.h_en.grid(row=1, column=1)
        self.resize_btn = tkinter.Button(self.resize_frame, text="Добавить",
                                         width=10, command=self.resize)
        self.resize_btn.grid(row=1, column=2)

    def get_q(self):
        return self.qs

    def add_q(self):
        # TODO: добавить обработку наличия входящей информации + валидацию
        x, y, q = self.x_en.get(), self.y_en.get(), self.q_en.get()
        if not x.isdigit() or not y.isdigit() or not q.isdigit():
            return
        x, y, q = int(x), int(y), int(q)
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

    def run(self):
        self.root.mainloop()


def run_app():
    gui = Gui()
    gui.run()


if __name__ == "__main__":
    app = Thread(target=run_app)
    app.start()
