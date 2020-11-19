import tkinter as tk
import webbrowser
from tkinter import ttk

import ensemblx.excel_page as excel_page


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        s = ttk.Style()
        s.configure('Title.TLabel', font=('Arial', 24), padding=[0, 10, 0, 0])
        s.configure('SectionTitle.TLabel', font=('Arial', 14), padding=[0, 0, 0, 10])
        s.configure('Tagline.TLabel', font=('Arial', 14), padding=[0, 0, 0, 10])
        s.configure('StartPage.TButton', font=('Arial', 14), width=25)
        s.configure('Copyright.TLabel', font=('Arial', 10), padding=[0, 25, 0, 0])
        s.configure('Warranty.TLabel', font=('Arial', 8), padding=[10, 5, 10, 0])
        s.configure('Redistribute.TLabel', font=('Arial', 8), padding=[10, 0, 10, 10])

        title = ttk.Label(self, text="EnsemblX", style='Title.TLabel')
        title.pack()

        tagline = ttk.Label(self, text="Barley Gene Annotation Reference", style='Tagline.TLabel')
        tagline.pack()

        title_tag_sep = ttk.Separator(self)
        title_tag_sep.pack(fill='both')

        options_frame = ttk.Frame(self)
        options_frame.pack(pady=10)

        tagline = ttk.Label(options_frame, text="Referencing Options:", font=('Arial', 14))
        tagline.pack(pady=15)

        excel_page_button = ttk.Button(options_frame, text="Reference with IDs from Excel",
                                       command=lambda: controller.show_frame(excel_page.ExcelPage),
                                       style='StartPage.TButton')
        excel_page_button.pack()

        excel_page_button = ttk.Button(options_frame, text="Quick Reference",
                                       command=lambda: controller.show_frame(excel_page.ExcelPage),
                                       style='StartPage.TButton')
        excel_page_button.pack()
        excel_page_button.state(['disabled'])

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

        github_button = ttk.Button(self, text="Code Repository",
                                   command=lambda: self.open_url('https://github.com/crlsmmns/ensemblx'),
                                   style='StartPage.TButton')
        github_button.pack(side='bottom')

        github_help_button = ttk.Button(self, text="Help Documentation",
                                        command=lambda: self.open_url('https://github.com/crlsmmns/ensemblx/wiki'),
                                        style='StartPage.TButton')
        github_help_button.pack(side='bottom')

        tagline = ttk.Label(self, text="EnsemblX on GitHub:", style='SectionTitle.TLabel')
        tagline.pack(side='bottom')

        github_licence_sep = ttk.Separator(self)
        github_licence_sep.pack(side='bottom', fill='both', pady=10)

    def open_url(self, url):
        webbrowser.open_new(url)
