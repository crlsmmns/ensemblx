import tkinter as tk

import ensemblx.excel_page as excel_page
import ensemblx.quick_reference_page as quick_reference_page
import ensemblx.start_page as start_page


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EnsemblX")

        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0)

        self.frames = {}

        for F in (start_page.StartPage, excel_page.ExcelPage, quick_reference_page.QuickReferencePage):
            frame = F(main_frame, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(start_page.StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
