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

        title = ttk.Label(self, text="EnsemblX", font=('Arial', 24))
        title.grid(column=1, row=0)

        tagline = ttk.Label(self, text="Automated High-Throughput Barley Gene Annotation Lookup", font=('Arial', 14))
        tagline.grid(column=0, row=2, columnspan=3)

        excel_page_button = ttk.Button(self, text="Import/Export Excel", command=lambda: controller.show_frame(ExcelPage))
        excel_page_button.grid(column=1, row=3)

        quick_reference_button = ttk.Button(self, text="Quick Reference",
                                       command=lambda: controller.show_frame(QuickReferencePage))
        quick_reference_button.grid(column=1, row=4)


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
        open_file_button = ttk.Button(self, text="Ensembl Ref")
        open_file_button.grid(column=2, row=0)

        go_button = ttk.Button(self, text="Go!")
        go_button.grid(column=3, row=0)

        start_page_button = ttk.Button(self, text="Start Page", command=lambda: controller.show_frame(StartPage))
        start_page_button.grid(column=2, row=1)



app = ExcelWindow()
app.mainloop()