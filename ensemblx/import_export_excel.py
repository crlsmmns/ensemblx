import pandas as pd
import json
import requests


def import_excel(file_path):
    # Read in all sheet in Excel file
    excel_sheets = pd.read_excel(file_path, sheet_name=None)

    #Returns dictionary of original Excel sheets (Key = Sheet Name, Value = Sheet Data)
    return excel_sheets


def ensembl_data(excel_sheets):
    # Loop through Excel sheets and pull down Ensembl Data from REST API
    for sheet in excel_sheets:
            # Setup for Ensembl REST API lookup by list of gene ids
            server = "https://rest.ensembl.org"
            ext = "/lookup/id"
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

            # Get list of Gene IDs from each sheet
            requested_ids = excel_sheets[sheet]['Gene ID'].tolist()

            # Define list of requested ids as compatible with a JSON POST request
            ids_requested = '{ "ids" : ' + json.dumps(requested_ids) + ' }'

            # POST the information request
            ensembl_response = requests.post(server + ext, headers=headers, data=ids_requested)
            ensembl_json = ensembl_response.json()
            ensembl_data = pd.DataFrame(ensembl_json).transpose()
            excel_sheets[sheet] = ensembl_data

    # Return sheet dictionary updated with new info
    return excel_sheets

excel_sheets = import_excel('../data/excel-test-set.xls')
ensembl_data = ensembl_data(excel_sheets)

