import tkinter
from tkinter import ttk, RIGHT, Y, BOTTOM, X, LEFT, YES, BOTH, SUNKEN
from PIL import Image, ImageTk


def init(self):
    self.qs = {}
    self.size = self.im_w, self.im_h = 700, 700
    self.image = Image.new('RGB', (self.im_w, self.im_h), 'white')
    # self.image = Image.open('0.png')
    self.root = tkinter.Tk()

    # Image
    self.image_frame = tkinter.Frame(self.root)
    self.image_frame.pack(side=LEFT)

    # Canvas
    self.canvas = tkinter.Canvas(self.image_frame, height=600, width=600,
                                 scrollregion=(0, 0, self.im_w, self.im_h), relief=SUNKEN
                                 )
    self.photo = ImageTk.PhotoImage(self.image)
    self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

    # Vertical bar
    self.vertibar = tkinter.Scrollbar(self.image_frame, orient=tkinter.VERTICAL)
    self.vertibar.config(command=self.canvas.yview)
    self.canvas.config(yscrollcommand=self.vertibar.set)
    self.vertibar.pack(side=RIGHT, fill=Y)

    # Horizontal bar
    self.horibar = tkinter.Scrollbar(self.image_frame, orient=tkinter.HORIZONTAL)
    self.horibar.config(command=self.canvas.xview)
    self.canvas.config(xscrollcommand=self.horibar.set)
    self.horibar.pack(side=BOTTOM, fill=X)

    self.canvas.pack(side=LEFT, expand=YES, fill=BOTH)

    # Data Frame
    self.data_frame = tkinter.Frame(self.root)
    self.data_frame.pack(side=RIGHT)
    # Q managing
    self.q_managing_frame = tkinter.Frame(self.data_frame)
    self.q_managing_frame.pack()

    # Input Frame
    self.input_frame = tkinter.Frame(self.q_managing_frame)
    self.input_frame.pack()

    self.x_l = tkinter.Label(self.input_frame, width=10, text='x')
    self.x_l.pack()
    self.y_l = tkinter.Label(self.input_frame, width=10, text='y')
    self.y_l.pack()
    self.q_l = tkinter.Label(self.input_frame, width=10, text='q')
    self.q_l.pack()
    self.x_en = tkinter.Entry(self.input_frame, width=10)
    self.x_en.pack()
    self.y_en = tkinter.Entry(self.input_frame, width=10)
    self.y_en.pack()
    self.q_en = tkinter.Entry(self.input_frame, width=10)
    self.q_en.pack()
    self.add_btn = tkinter.Button(self.input_frame, text="Добавить",
                                  width=10, command=self.add_q)
    self.add_btn.pack()

    # List Frame
    self.list_frame = tkinter.Frame(self.q_managing_frame)
    self.list_frame.pack()

    self.q_list = ttk.Treeview(self.list_frame)
    self.q_list.pack()

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
    self.resize_frame.pack()

    self.w_l = tkinter.Label(self.resize_frame, width=10, text=f'width: {self.im_w}')
    self.w_l.pack()
    self.h_l = tkinter.Label(self.resize_frame, width=10, text=f'height: {self.im_h}')
    self.h_l.pack()
    self.w_en = tkinter.Entry(self.resize_frame, width=10)
    self.w_en.pack()
    self.h_en = tkinter.Entry(self.resize_frame, width=10)
    self.h_en.pack()
    self.resize_btn = tkinter.Button(self.resize_frame, text="Добавить",
                                     width=10, command=self.resize)
    self.resize_btn.pack()

    self.calc_hook_btn = tkinter.Button(self.data_frame, text='calc_hook')
    self.calc_hook_btn.pack()
    self.draw_hook_btn = tkinter.Button(self.data_frame, text='draw_hook')
    self.draw_hook_btn.pack()
    self.show_close_hook_btn = tkinter.Button(self.data_frame, text='show_close_hook')
    self.show_close_hook_btn.pack()
