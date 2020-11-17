import tkinter as tk
from tkinter import ttk

import ensemblx.excel_page as excel_page


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        s = ttk.Style()
        s.configure('Title.TLabel', font=('Arial', 24), padding=[0, 10, 0, 0])
        s.configure('Tagline.TLabel', font=('Arial', 14), padding=[0, 0, 0, 25])
        s.configure('StartPage.TButton', font=('Arial', 14), width=20)
        s.configure('Copyright.TLabel', font=('Arial', 10), padding=[0, 25, 0, 0])
        s.configure('Warranty.TLabel', font=('Arial', 8), padding=[10, 5, 10, 0])
        s.configure('Redistribute.TLabel', font=('Arial', 8), padding=[10, 0, 10, 10])

        title = ttk.Label(self, text="EnsemblX", style='Title.TLabel')
        title.pack()

        tagline = ttk.Label(self, text="Barley Gene Annotation Lookup", style='Tagline.TLabel')
        tagline.pack()

        excel_page_button = ttk.Button(self, text="Use IDs from Excel",
                                       command=lambda: controller.show_frame(excel_page.ExcelPage),
                                       style='StartPage.TButton')
        excel_page_button.pack()

        redistribute_label = ttk.Label(self,
                                       text='This is free software, and you are welcome to redistribute it under '
                                            'certain conditions.',
                                       style='Redistribute.TLabel')
        redistribute_label.pack(side='bottom')

        warranty_label = ttk.Label(self, text='This program comes with ABSOLUTELY NO WARRANTY.',
                                   style='Warranty.TLabel')
        warranty_label.pack(side='bottom')

        copyright_label = ttk.Label(self, text='EnsemblX Copyright (C) 2020 Carl H. Simmons', style='Copyright.TLabel')
        copyright_label.pack(side='bottom')
