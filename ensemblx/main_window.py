import tkinter as tk
from tkinter import ttk

import ensemblx.excel_page as excel_page
import ensemblx.start_page as start_page


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EnsemblX")

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0)

        self.frames = {}

        for Frames in (start_page.StartPage, excel_page.ExcelPage):
            frame = Frames(main_frame, self)

            self.frames[Frames] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(start_page.StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
