import pandas as pd
import json
import requests
import tkinter as tk
from tkinter import ttk

from tkinter import filedialog as fd

# filename = fd.askopenfilename()
#
#
# def import_excel(file_path):
#     # Read in all sheet in Excel file
#     excel_sheets = pd.read_excel(file_path, sheet_name=None)
#
#     #Returns dictionary of original Excel sheets (Key = Sheet Name, Value = Sheet Data)
#     return excel_sheets
#
#
# def run_ensembl_api(excel_sheets):
#     # Loop through Excel sheets and pull down Ensembl Data from REST API
#     for sheet in excel_sheets:
#         # Setup for Ensembl REST API lookup by list of gene ids
#         server = "https://rest.ensembl.org"
#         ext = "/lookup/id"
#         headers = {"Content-Type": "application/json", "Accept": "application/json"}
#
#         # Get list of Gene IDs from each sheet
#         requested_ids = excel_sheets[sheet]['Gene ID'].tolist()
#
#         # Define list of requested ids as compatible with a JSON POST request
#         ids_requested = '{ "ids" : ' + json.dumps(requested_ids) + ' }'
#
#         # POST the information request
#         ensembl_response = requests.post(server + ext, headers=headers, data=ids_requested)
#         ensembl_json = ensembl_response.json()
#         ensembl_df = pd.DataFrame(ensembl_json).transpose()
#         ensembl_df = ensembl_df.add_prefix('ensembl_')
#         excel_sheets[sheet].columns = ['gene_id']
#         ensembl_data = excel_sheets[sheet].merge(ensembl_df, how='left', left_on='gene_id', right_on='ensembl_id')
#         excel_sheets[sheet] = ensembl_data
#         print('Api Check!')
#
#     # Return sheet dictionary updated with new info
#     return excel_sheets
#
#
# def add_barlex_data(ensembl_data):
#     # Import preprocessed BARLEX data from 'barlex_df.csv'
#     barlex_df = pd.read_csv('../data/barlex_df.csv')
#
#     # Clean id strings into lists of ids
#     cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
#     for col in cols_to_list:
#         barlex_df[col] = barlex_df[col].str.split(pat=', ').tolist()
#
#     barlex_df = barlex_df.add_prefix('barlex_')
#
#     for sheet in ensembl_data:
#         ensembl_barlex_data = ensembl_data[sheet].merge(barlex_df, how='left', left_on='gene_id', right_on='barlex_gene_id')
#         ensembl_data[sheet] = ensembl_barlex_data
#         print('Barlex Merge!')
#     return ensembl_data
#
#
# def export_excel(ensembl_barlex_data):
#     with pd.ExcelWriter('../data/excel-test-set-output.xlsx') as writer:
#         for sheet in ensembl_barlex_data:
#             ensembl_barlex_data[sheet].to_excel(writer, sheet_name=sheet)
#
#
# excel_sheets = import_excel(filename)
# ensembl_data = run_ensembl_api(excel_sheets)
# ensembl_barlex_data = add_barlex_data(ensembl_data)
# export_excel(ensembl_barlex_data)


class ExcelWindow(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("EnsemblX")

        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0)

        self.frames = {}

        for F in (StartPage, ExcelPage, QuickReferencePage):
            frame = F(main_frame, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        s = ttk.Style()
        s.configure('EnsemblXTitle.TLabel', font=('Arial', 24), padding=[0, 10, 0, 0])
        s.configure('EnsemblXTagline.TLabel', font=('Arial', 14), padding=[0, 0, 0, 10])
        s.configure('StartPage.TButton', font=('Arial', 14), padding=[50, 5], width=16)
        s.configure('Copyright.TLabel', font=('Arial', 10), padding=[0, 10, 0, 0])
        s.configure('Warranty.TLabel', font=('Arial', 8), padding=[10, 5, 10, 0])
        s.configure('Redistribute.TLabel', font=('Arial', 8), padding=[10, 0, 10, 10])

        title = ttk.Label(self, text="EnsemblX", style='EnsemblXTitle.TLabel')
        title.grid(column=1, row=0)

        tagline = ttk.Label(self, text="Automated Barley Gene Annotation Lookup", style='EnsemblXTagline.TLabel')
        tagline.grid(column=0, row=2, columnspan=3)

        excel_page_button = ttk.Button(self, text="Import from Excel", command=lambda: controller.show_frame(ExcelPage), style='StartPage.TButton')
        excel_page_button.grid(column=1, row=3)

        quick_reference_button = ttk.Button(self, text="Quick Reference",
                                       command=lambda: controller.show_frame(QuickReferencePage), style='StartPage.TButton')
        quick_reference_button.grid(column=1, row=4)

        copyright_label = ttk.Label(self, text='EnsemblX Copyright (C) 2020 Carl H. Simmons', style='Copyright.TLabel')
        copyright_label.grid(column=0, row=5, columnspan=3)

        warranty_label = ttk.Label(self, text='This program comes with ABSOLUTELY NO WARRANTY.', style='Warranty.TLabel')
        warranty_label.grid(column=0, row=6, columnspan=3)

        redistribute_label = ttk.Label(self, text='This is free software, and you are welcome to redistribute it under certain conditions.', style='Redistribute.TLabel')
        redistribute_label.grid(column=0, row=7, columnspan=3)



class ExcelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        open_file_button = ttk.Button(self, text="Find File")
        open_file_button.grid(column=2, row=0)

        go_button = ttk.Button(self, text="Run Annotations")
        go_button.grid(column=3, row=0)

        start_page_button = ttk.Button(self, text="Start Page", command=lambda: controller.show_frame(StartPage))
        start_page_button.grid(column=2, row=1)

class QuickReferencePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        title_quick = ttk.Label(self, text="Quick Reference", font=('Arial', 20))
        title_quick.grid(column=0, row=0)

        # Initialize variables
        gene_id = tk.StringVar()

        # Clear and reform frame
        output_frame = tk.Frame(self)
        output_frame.grid(column=0, row=3)

        # Create input interactions
        entry_frame = tk.Frame(self)
        entry_frame.grid(column=0, row=1)

        entry_label = ttk.Label(entry_frame, text="Enter Gene ID:", font=('Arial', 16))
        entry_label.grid(column=0, row=0)

        entry_box = ttk.Entry(entry_frame, width=20, textvariable=gene_id)
        entry_box.grid(column=1, row=0)

        entry_button = ttk.Button(entry_frame, text="Go")
        entry_button.grid(column=2, row=0)

        # Create output source selector
        source_select_frame = tk.Frame(self)
        source_select_frame.grid(column=0, row=2)

        source_selected = tk.IntVar()
        source_selected.set(1)

        source_select_barlex = ttk.Radiobutton(source_select_frame, text='BARLEX: CDS HC May 2016', value=1,
                                               variable=source_selected)
        source_select_barlex.grid(column=0, row=0)

        source_select_ensembl = ttk.Radiobutton(source_select_frame, text='Ensembl API', value=2,
                                                variable=source_selected)
        source_select_ensembl.grid(column=1, row=0)



app = ExcelWindow()
app.mainloop()