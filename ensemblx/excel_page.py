import json
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pandas as pd
import requests

import ensemblx.start_page as start_page


class ExcelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        s = ttk.Style()
        s.configure('SecondaryTitle.TLabel', font=('Arial', 14), padding=[0, 0, 0, 0])
        s.configure('Instructions.TLabel', font=('Arial', 12), padding=[0, 10, 0, 0])

        frame1 = tk.Frame(self)
        frame1.pack()

        title = ttk.Label(frame1, text="Use IDs from Excel", style='SecondaryTitle.TLabel')
        title.pack()

        frame2 = tk.Frame(self)
        frame2.pack()

        step_1_instruct = ttk.Label(frame2, text='Step 1: Press "Select File" and choose an Excel document.',
                                    style='Instructions.TLabel')
        step_1_instruct.pack()

        get_file_button = ttk.Button(frame2, text="Select File",
                                     command=lambda: self.excel_processing(),
                                     style='StartPage.TButton')
        get_file_button.pack()

        selected_file_frame = tk.Frame(frame2)
        selected_file_frame.pack()

        file_selected_label = ttk.Label(selected_file_frame, text='File Selected:',
                                        style='Instructions.TLabel',
                                        font='bold')

        file_selected_label.pack(side='left')
        file_selected = ttk.Label(selected_file_frame, text='blahblahblah.xlsx',
                                  style='Instructions.TLabel',
                                  font='bold')
        file_selected.pack(side='left')

        frame3 = tk.Frame(self)
        frame3.pack()

        step_2_instruct = ttk.Label(frame3, text='Step 2: Check desired annotation sources.',
                                    style='Instructions.TLabel')
        step_2_instruct.pack()

        frame4 = tk.Frame(self)
        frame4.pack()

        self.check_ensembl = tk.IntVar()

        check_ensembl_button = ttk.Checkbutton(frame4, text="Ensembl Rest API", variable=self.check_ensembl)
        check_ensembl_button.pack(side='left')

        self.check_barlex = tk.IntVar()

        check_barlex_button = ttk.Checkbutton(frame4, text="BARLEX: CDS HC May 2016", variable=self.check_barlex)
        check_barlex_button.pack(side='left')

        frame5 = tk.Frame(self)
        frame5.pack(side='bottom', padx=10, pady=10)

        return_button = ttk.Button(frame5, text="Return to Start Page",
                                   command=lambda: controller.show_frame(start_page.StartPage))
        return_button.pack()

    def get_file(self):
        self.filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        print(self.filename)

    def read_excel(self):
        self.excel_sheets = pd.read_excel(self.filename, sheet_name=None)

    def run_ensembl_api(self):
        for sheet in self.excel_sheets:
            server = "https://rest.ensembl.org"
            ext = "/lookup/id"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

            requested_ids = self.excel_sheets[sheet]['Gene ID'].tolist()

            ids_requested = '{ "ids" : ' + json.dumps(requested_ids) + ' }'

            ensembl_response = requests.post(server + ext, headers=headers, data=ids_requested)
            ensembl_json = ensembl_response.json()
            ensembl_df = pd.DataFrame(ensembl_json).transpose()
            ensembl_df = ensembl_df.add_prefix('ensembl_')
            self.excel_sheets[sheet].columns = ['gene_id']
            ensembl_data = self.excel_sheets[sheet].merge(ensembl_df, how='left', left_on='gene_id',
                                                          right_on='ensembl_id')
            self.excel_sheets[sheet] = ensembl_data
            print('Api Check!')

    def add_barlex_data(self):
        barlex_df = pd.read_csv('data/barlex_clean_df.csv')

        cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
        for col in cols_to_list:
            barlex_df[col] = barlex_df[col].str.split(pat=', ').tolist()

        barlex_df = barlex_df.add_prefix('barlex_')

        for sheet in self.excel_sheets:
            ensembl_barlex_data = self.excel_sheets[sheet].merge(barlex_df, how='left', left_on='gene_id',
                                                                 right_on='barlex_gene_id')
            self.excel_sheets[sheet] = ensembl_barlex_data
            print('Barlex Merge!')

    def get_save(self):
        self.savefilename = asksaveasfilename(
            defaultextension='.xlsx')  # show an "Open" dialog box and return the path to the selected file
        print(self.savefilename)

    def write_excel(self):
        with pd.ExcelWriter(self.savefilename) as writer:
            for sheet in self.excel_sheets:
                self.excel_sheets[sheet].to_excel(writer, sheet_name=sheet)

    def excel_processing(self):
        self.get_file()
        self.read_excel()
        self.run_ensembl_api()
        self.add_barlex_data()
        self.get_save()
        self.write_excel()
