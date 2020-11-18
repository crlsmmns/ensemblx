import json
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from os import system
from sys import platform

import pandas as pd
import requests
import re

import ensemblx.start_page as start_page


class ExcelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        s = ttk.Style()
        s.configure('Instructions.TLabel', font=('Arial', 12), padding=[0, 10, 0, 10])
        s.configure('FileButtons.TButton', font=('Arial', 14), width=20)
        s.configure('Checkboxes.TCheckbutton', padding=[5, 0, 5, 10])

        frame1 = tk.Frame(self)
        frame1.pack()

        title = ttk.Label(frame1, text="Look up annotations with IDs from Excel", style='SecondaryTitle.TLabel', font=('Arial', 14))
        title.pack(pady=5)

        title_sep = ttk.Separator(self)
        title_sep.pack(fill='both')

        frame2 = tk.Frame(self)
        frame2.pack()

        step_1_instruct = ttk.Label(frame2, text='Step 1: Click "Select File" and choose an Excel document.',
                                    style='Instructions.TLabel')
        step_1_instruct.pack()

        get_file_button = ttk.Button(frame2, text="Select File",
                                     command=lambda: self.get_file(),
                                     style='FileButtons.TButton')
        get_file_button.pack()

        selected_file_frame = tk.Frame(frame2)
        selected_file_frame.pack()

        file_selected_label = ttk.Label(selected_file_frame, text='File Selected:',
                                        font=('Arial', 10, 'bold'), padding=[0, 10, 0, 10])

        file_selected_label.pack(side='left')

        self.file_selected = ttk.Label(selected_file_frame, text='None',
                                  font=('Arial', 10, 'italic'), padding=[0, 10, 0, 10])
        self.file_selected.pack(side='left')

        step_1_sep = ttk.Separator(self)
        step_1_sep.pack(fill='both')

        frame3 = tk.Frame(self)
        frame3.pack()

        step_2_instruct = ttk.Label(frame3, text='Step 2: Check at least 1 annotation source.',
                                    style='Instructions.TLabel')
        step_2_instruct.pack()

        frame4 = tk.Frame(self)
        frame4.pack()

        self.check_ensembl = tk.IntVar()

        self.check_ensembl_button = ttk.Checkbutton(frame4, text="Ensembl REST API", variable=self.check_ensembl, style='Checkboxes.TCheckbutton',
                                               command=lambda: self.check_active_sources())
        self.check_ensembl_button.pack(side='left')
        self.check_ensembl_button.state(['disabled'])

        self.check_barlex = tk.IntVar()

        self.check_barlex_button = ttk.Checkbutton(frame4, text="BARLEX: CDS HC May 2016", variable=self.check_barlex, style='Checkboxes.TCheckbutton',
                                              command=lambda: self.check_active_sources())
        self.check_barlex_button.pack(side='left')
        self.check_barlex_button.state(['disabled'])

        step_2_sep = ttk.Separator(self)
        step_2_sep.pack(fill='both')

        frame5 = tk.Frame(self)
        frame5.pack()

        step_3_instruct = ttk.Label(frame5, text='Step 3: Start data processing.',
                                    style='Instructions.TLabel')
        step_3_instruct.pack()

        self.progress_bar = ttk.Progressbar(frame5, length=200)
        self.progress_bar.pack(side='left')

        self.go_button = ttk.Button(frame5, text='Start', command=lambda: self.excel_processing())
        self.go_button.state(['disabled'])
        self.go_button.pack(side='left', padx=5)

        print(self.go_button)

        frame6 = tk.Frame(self)
        frame6.pack()

        self.progress_text = ttk.Label(frame6, text='Waiting to start', font=('Arial', 10, 'italic'))
        self.progress_text.pack(pady=10)

        step_3_sep = ttk.Separator(self)
        step_3_sep.pack(fill='both')

        frame7 = tk.Frame(self)
        frame7.pack()

        step_2_instruct = ttk.Label(frame7, text='Step 4: Open the annotated Excel file.',
                                    font=('Arial', 12), padding=[0, 10, 0, 0])
        step_2_instruct.pack()

        self.open_output_button = ttk.Button(frame7, text='Open Output', command=lambda: self.open_output(), style='FileButtons.TButton')
        self.open_output_button.pack(pady=10)
        self.open_output_button.state(['disabled'])

        step_4_sep = ttk.Separator(self)
        step_4_sep.pack(fill='both')

        frame8 = tk.Frame(self)
        frame8.pack(side='bottom')

        return_button = ttk.Button(frame8, text="Return to Start Page",
                                   command=lambda: self.return_to_start(controller))
        return_button.pack(pady=10)

    def get_file(self):
        self.filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.check_active_input()
        self.filename_short = re.search(r'\/([^\/]*)$', self.filename).group(1)
        self.file_selected.config(text=self.filename_short)
        self.progress_bar['value'] = 0
        self.progress_bar.update_idletasks()

    def read_excel(self):
        self.excel_sheets = pd.read_excel(self.filename, sheet_name=None)

    def progress_steps(self):
        steps = 2
        if self.check_ensembl.get():
            steps += len(self.excel_sheets)
        if self.check_barlex.get():
            steps += 1
        self.progress_step = 100 / steps

    def run_ensembl_api(self):
        server = "https://rest.ensembl.org"
        ext = "/lookup/id"
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        for index, sheet in enumerate(self.excel_sheets):
            self.progress_bar['value'] += self.progress_step
            self.progress_bar.update_idletasks()
            self.progress_text.config(text=('Requesting data from Ensembl (' + sheet + ')'), font=('Arial', 10, 'italic'))
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
            print('Api Check!')

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
            self.progress_text.config(text=('Merging local BARLEX data: ' + sheet), font=('Arial', 10, 'italic'))
            self.progress_text.update_idletasks()
            print('Barlex Merge!')

    def get_save(self):
        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update_idletasks()
        self.progress_text.config(text='Waiting for save location', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        self.savefilename = asksaveasfilename(filetypes=[('Excel Files (XLSX)', '*.xlsx'), ('Excel Files (XLS)', '*.xls')],
            defaultextension='.xlsx')
        print(self.savefilename) # show an "Open" dialog box and return the path to the selected file

    def write_excel(self):
        self.progress_text.config(text='Writing output to Excel file', font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        writer = pd.ExcelWriter(self.savefilename)
        for sheet in self.excel_sheets:
            self.excel_sheets[sheet].to_excel(writer, sheet_name=sheet)
            print(sheet)
        writer.save()
        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update_idletasks()
        print('Write!')

    def excel_processing(self):
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
        self.progress_text.config(text=('Processing of "' + self.filename_short + '" complete!'), font=('Arial', 10, 'italic'))
        self.progress_text.update_idletasks()
        self.open_output_button.state(['!disabled'])
        print('Done!')

    def return_to_start(self, controller):
        controller.show_frame(start_page.StartPage)
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
            print(self.filename)
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
        if platform == "win32":
            system('start ' + self.savefilename)
        else:
            system('open ' + self.savefilename)
