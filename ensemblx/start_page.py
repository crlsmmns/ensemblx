import tkinter as tk
from tkinter import ttk

import ensemblx.excel_page as excel_page
import ensemblx.quick_reference_page as quick_reference_page


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        s = ttk.Style()
        s.configure('Title.TLabel', font=('Arial', 24), padding=[0, 10, 0, 0])
        s.configure('Tagline.TLabel', font=('Arial', 14), padding=[0, 0, 0, 50])
        s.configure('StartPage.TButton', font=('Arial', 14), padding=[50, 5], width=16)
        s.configure('Copyright.TLabel', font=('Arial', 10), padding=[0, 50, 0, 0])
        s.configure('Warranty.TLabel', font=('Arial', 8), padding=[10, 5, 10, 0])
        s.configure('Redistribute.TLabel', font=('Arial', 8), padding=[10, 0, 10, 10])

        title = ttk.Label(self, text="EnsemblX", style='Title.TLabel')
        title.pack()

        tagline = ttk.Label(self, text="Automated Barley Gene Annotation Lookup", style='Tagline.TLabel')
        tagline.pack()

        excel_page_button = ttk.Button(self, text="Import from Excel",
                                       command=lambda: controller.show_frame(excel_page.ExcelPage),
                                       style='StartPage.TButton')
        excel_page_button.pack()

        quick_reference_button = ttk.Button(self, text="Quick Reference",
                                            command=lambda: controller.show_frame(
                                                quick_reference_page.QuickReferencePage), style='StartPage.TButton')
        quick_reference_button.pack()

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
