import json
import re
import subprocess
import sys
import tkinter as tk
import webbrowser
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pandas as pd
import requests


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EnsemblX")

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0)

        self.frames = {}

        for Frames in (StartPage, ExcelPage):
            frame = Frames(main_frame, self)

            self.frames[Frames] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


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
                                       command=lambda: controller.show_frame(ExcelPage),
                                       style='StartPage.TButton')
        excel_page_button.pack()

        excel_page_button = ttk.Button(options_frame, text="Quick Reference",
                                       command=lambda: controller.show_frame(ExcelPage),
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

    @staticmethod
    def open_url(url):
        webbrowser.open_new(url)


class ExcelPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        s = ttk.Style()
        s.configure('Instructions.TLabel', font=('Arial', 12), padding=[0, 10, 0, 10])
        s.configure('FileButtons.TButton', font=('Arial', 14), width=20)
        s.configure('Checkboxes.TCheckbutton', padding=[5, 0, 5, 10])
        s.configure('Failed.Horizontal.TProgressbar', foreground='red', background='red')

        frame1 = ttk.Frame(self)
        frame1.pack()

        title = ttk.Label(frame1, text="Reference annotations with IDs from Excel", style='SecondaryTitle.TLabel',
                          font=('Arial', 14))
        title.pack(pady=5)

        title_sep = ttk.Separator(self)
        title_sep.pack(fill='both')

        frame2 = ttk.Frame(self)
        frame2.pack()

        step_1_instruct = ttk.Label(frame2, text='Step 1: Click "Select File" and choose an Excel document.',
                                    style='Instructions.TLabel')
        step_1_instruct.pack()

        get_file_button = ttk.Button(frame2, text="Select File",
                                     command=lambda: self.get_file(),
                                     style='FileButtons.TButton')
        get_file_button.pack()

        selected_file_frame = ttk.Frame(frame2)
        selected_file_frame.pack()

        file_selected_label = ttk.Label(selected_file_frame, text='File Selected:',
                                        font=('Arial', 10, 'bold'), padding=[0, 10, 0, 10])

        file_selected_label.pack(side='left')

        self.file_selected = ttk.Label(selected_file_frame, text='None',
                                       font=('Arial', 10, 'italic'), padding=[0, 10, 0, 10])
        self.file_selected.pack(side='left')

        step_1_sep = ttk.Separator(self)
        step_1_sep.pack(fill='both')

        frame3 = ttk.Frame(self)
        frame3.pack()

        step_2_instruct = ttk.Label(frame3, text='Step 2: Check at least 1 annotation source.',
                                    style='Instructions.TLabel')
        step_2_instruct.pack()

        frame4 = ttk.Frame(self)
        frame4.pack()

        self.check_ensembl = tk.IntVar()

        self.check_ensembl_button = ttk.Checkbutton(frame4, text="Ensembl REST API", variable=self.check_ensembl,
                                                    style='Checkboxes.TCheckbutton',
                                                    command=lambda: self.check_active_sources())
        self.check_ensembl_button.pack(side='left')
        self.check_ensembl_button.state(['disabled'])

        self.check_barlex = tk.IntVar()

        self.check_barlex_button = ttk.Checkbutton(frame4, text="BARLEX: CDS HC May 2016", variable=self.check_barlex,
                                                   style='Checkboxes.TCheckbutton',
                                                   command=lambda: self.check_active_sources())
        self.check_barlex_button.pack(side='left')
        self.check_barlex_button.state(['disabled'])

        step_2_sep = ttk.Separator(self)
        step_2_sep.pack(fill='both')

        frame5 = ttk.Frame(self)
        frame5.pack()

        step_3_instruct = ttk.Label(frame5, text='Step 3: Start data processing.',
                                    style='Instructions.TLabel')
        step_3_instruct.pack()

        self.progress_bar = ttk.Progressbar(frame5, length=200)
        self.progress_bar.pack(side='left')

        self.go_button = ttk.Button(frame5, text='Start', command=lambda: self.excel_processing())
        self.go_button.state(['disabled'])
        self.go_button.pack(side='left', padx=5)

        frame6 = ttk.Frame(self)
        frame6.pack()

        self.progress_text = ttk.Label(frame6, text='Waiting to start', font=('Arial', 10, 'italic'))
        self.progress_text.pack(pady=10)

        step_3_sep = ttk.Separator(self)
        step_3_sep.pack(fill='both')

        frame7 = ttk.Frame(self)
        frame7.pack()

        step_2_instruct = ttk.Label(frame7, text='Step 4: Open the annotated Excel file.',
                                    font=('Arial', 12), padding=[0, 10, 0, 0])
        step_2_instruct.pack()

        self.open_output_button = ttk.Button(frame7, text='Open Output', command=lambda: self.open_output(),
                                             style='FileButtons.TButton')
        self.open_output_button.pack(pady=10)
        self.open_output_button.state(['disabled'])

        step_4_sep = ttk.Separator(self)
        step_4_sep.pack(fill='both')

        frame8 = ttk.Frame(self)
        frame8.pack(side='bottom')

        return_button = ttk.Button(frame8, text="Return to Start Page",
                                   command=lambda: self.return_to_start(controller))
        return_button.pack(pady=10)

    def get_file(self):
        self.filename = askopenfilename(title="Select file",
                                        filetypes=[('Excel Spreadsheets', '*.xls;*.xlsx;*.xlsm;*.xlsb'),
                                                   ('OpenOffice Spreadsheets', '*.ods')])
        self.check_active_input()
        self.filename_short = re.search(r'\/([^\/]*)$', self.filename).group(1)
        self.file_selected.config(text=self.filename_short)
        self.progress_bar['value'] = 0
        self.progress_bar.update_idletasks()

    def read_excel(self):
        self.excel_sheets = pd.read_excel(self.filename, sheet_name=None)

    def progress_steps(self):
        steps = 1
        if self.check_ensembl.get():
            steps += len(self.excel_sheets)
        if self.check_barlex.get():
            steps += 1
        self.progress_step = 90 / steps

    def run_ensembl_api(self):
        server = "https://rest.ensembl.org"
        ext = "/lookup/id"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        for index, sheet in enumerate(self.excel_sheets):
            self.progress_bar['value'] += self.progress_step
            self.progress_bar.update_idletasks()
            self.progress_text.config(text=('Requesting data from Ensembl (' + sheet + ')'),
                                      font=('Arial', 10, 'italic'))
            self.progress_text.update_idletasks()

            requested_ids = self.excel_sheets[sheet]['Gene ID'].tolist()

            ids_requested = '{ "ids" : ' + json.dumps(requested_ids) + ' }'

            ensembl_response = requests.post(server + ext, headers=headers, data=ids_requested)
            ensembl_json = ensembl_response.json()
            ensembl_df = pd.DataFrame(ensembl_json).transpose()
            ensembl_df = ensembl_df.add_prefix('ensembl_')
            ensembl_data = self.excel_sheets[sheet].merge(ensembl_df, how='left', left_on='Gene ID',
                                                          right_on='ensembl_id')
            self.excel_sheets[sheet] = ensembl_data

    def add_barlex_data(self):
        self.progress_text.config(text='Merging local BARLEX data', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()

        barlex_df = pd.read_csv('data/barlex_clean_df.csv')

        cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
        for col in cols_to_list:
            barlex_df[col] = barlex_df[col].str.split(pat=', ').tolist()

        barlex_df = barlex_df.add_prefix('barlex_')

        for index, sheet in enumerate(self.excel_sheets):
            ensembl_barlex_data = self.excel_sheets[sheet].merge(barlex_df, how='left', left_on='Gene ID',
                                                                 right_on='barlex_gene_id')
            self.excel_sheets[sheet] = ensembl_barlex_data

        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update_idletasks()
        self.progress_text.config(text='Merging local BARLEX data', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()

    def get_save(self):
        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update_idletasks()
        self.progress_text.config(text='Waiting for save location', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        self.savefilename = asksaveasfilename(
            filetypes=[('All Files', '*.*')],
            defaultextension='.xlsx')

    def write_excel(self):
        self.progress_text.config(text='Writing output to Excel file', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        writer = pd.ExcelWriter(self.savefilename)
        for sheet in self.excel_sheets:
            self.excel_sheets[sheet].to_excel(writer, sheet_name=sheet)
        writer.save()
        self.progress_bar['value'] += 10
        self.progress_bar.update_idletasks()
        self.progress_text.config(text=('Processing of "' + self.filename_short + '" complete!'),
                                  font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        self.open_output_button.state(['!disabled'])

    def excel_processing(self):
        try:
            self.progress_bar['value'] = 0
            self.progress_bar.update_idletasks()
            self.progress_text.config(text='Reading input from Excel file', font=('Arial', 10, 'italic'))
            self.progress_text.update_idletasks()
            self.read_excel()
            self.progress_steps()
            if self.check_ensembl.get():
                self.run_ensembl_api()
            if self.check_barlex.get():
                self.add_barlex_data()
            self.get_save()
            self.write_excel()
        except Exception as processing_error:
            self.progress_text.config(text='Process failed. Please check errors and restart.',
                                      font=('Arial', 10, 'italic'))
            self.progress_text.update_idletasks()
            messagebox.showerror(title='Ensemblx', message=processing_error)

    def return_to_start(self, controller):
        controller.show_frame(StartPage)
        self.filename = 'None'
        self.file_selected.config(text='None')
        self.check_active_input()
        self.check_ensembl.set(0)
        self.check_barlex.set(0)
        self.progress_bar['value'] = 0
        self.progress_bar.update_idletasks()
        self.progress_text.config(text='Waiting for start', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        self.open_output_button.state(['disabled'])

    def check_active_sources(self):
        if self.check_ensembl.get() or self.check_barlex.get():
            self.go_button.state(['!disabled'])
        else:
            self.go_button.state(['disabled'])

    def check_active_input(self):
        try:
            print(self.filename)  # Crude way to test if this object attribute exists (to generate AttributeError)
            if self.filename == 'None':
                self.check_ensembl_button.state(['disabled'])
                self.check_barlex_button.state(['disabled'])
            else:
                self.check_ensembl_button.state(['!disabled'])
                self.check_barlex_button.state(['!disabled'])
        except AttributeError:
            self.check_ensembl_button.state(['disabled'])
            self.check_barlex_button.state(['disabled'])

    def open_output(self):
        if sys.platform == "win32":
            print(self.savefilename)
            subprocess.call(['start', self.savefilename], shell=True)
        else:
            subprocess.call(['start', self.savefilename], shell=True)


ensemblx_gui = MainWindow()
ensemblx_gui.mainloop()
