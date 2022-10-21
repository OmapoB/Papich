from tkinter import *


class MainWindow:
    def __init__(self, master):
        self.main_window = master
        self.main_window.title('PapichLoh.exe')
        self.main_window.geometry(f'{280}x{90}')
        self.main_window.resizable(False, False)
        self.main_window.columnconfigure([0, 1], minsize=100)
        self.main_window.rowconfigure([0, 1, 2], minsize=20)
        self.label_from = Label(text='Откуда')
        self.label_from.grid(row=0, column=0)
        self.input_from = Entry()
        self.input_from.grid(row=0, column=1)
        self.label_to = Label(text='Куда')
        self.label_to.grid(row=1, column=0)
        self.input_to = Entry()
        self.input_to.grid(row=1, column=1)
        self.submit = Button(text='+10%', width=10)
        self.submit.grid(row=2, column=1, sticky='e')

    def get_input_from(self):
        return self.input_from.get()

    def get_input_to(self):
        return self.input_to.get()
