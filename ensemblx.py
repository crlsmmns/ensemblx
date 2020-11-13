import pandas as pd
import re
import requests
from tkinter import *


def barlex_data(*args):
    try:
        # Retrieve specified entry
        barlex_entry = barlex_df.loc[gene_id.get()]

        # Initialize variables
        barlex_annotation_str = StringVar()
        gene_transcript_id_str = StringVar()
        gene_location_str = StringVar()
        gene_class_str = StringVar()
        go_term_str = StringVar()
        pfam_id_str = StringVar()
        interpro_id_str = StringVar()

        # Set output variables from entry
        barlex_annotation = barlex_entry['barlex_annotation']
        barlex_annotation_str.set(barlex_annotation)

        gene_transcript_id = barlex_entry['gene_transcript_id']
        gene_transcript_id_str.set(gene_transcript_id)

        gene_location = barlex_entry['gene_location']
        gene_location_str.set(gene_location)

        gene_class = barlex_entry['gene_class']
        gene_class_str.set(gene_class)

        go_term_list = barlex_entry['go_terms']
        go_term_str.set(", ".join(go_term_list))

        pfam_id_list = barlex_entry['pfam_id']
        pfam_id_str.set(", ".join(pfam_id_list))

        interpro_id_list = barlex_entry['interpro_id']
        interpro_id_str.set(", ".join(interpro_id_list))

        # Set up global output variables
        output_frame_clear()

        global output_frame

        global label_0_0
        global label_0_1
        global label_0_2
        global label_0_3
        global label_0_4
        global label_0_5
        global label_0_6

        global label_1_0
        global label_1_1
        global label_1_2
        global label_1_3
        global label_1_4
        global label_1_5
        global label_1_6

        # Display outputs
        output_labels_width = 20
        output_variables_width = 70

        label_0_0 = Label(output_frame, text='BARLEX Annotation:', anchor='e', width=output_labels_width)
        label_0_0.grid(column=0, row=0)

        label_0_1 = Label(output_frame, text='Transcript ID:', anchor='e', width=output_labels_width)
        label_0_1.grid(column=0, row=1)

        label_0_2 = Label(output_frame, text='Gene Location:', anchor='e', width=output_labels_width)
        label_0_2.grid(column=0, row=2)

        label_0_3 = Label(output_frame, text='Gene Class:', anchor='e', width=output_labels_width)
        label_0_3.grid(column=0, row=3)

        label_0_4 = Label(output_frame, text='GO Terms:', anchor='e', width=output_labels_width)
        label_0_4.grid(column=0, row=4)

        label_0_5 = Label(output_frame, text='Pfam Protein Families:', anchor='e', width=output_labels_width)
        label_0_5.grid(column=0, row=5)

        label_0_6 = Label(output_frame, text='InterPro Protein Families:', anchor='e', width=output_labels_width)
        label_0_6.grid(column=0, row=6)

        label_1_0 = Label(output_frame, textvariable=barlex_annotation_str, anchor='w', width=output_variables_width)
        label_1_0.grid(column=1, row=0)

        label_1_1 = Label(output_frame, textvariable=gene_transcript_id_str, anchor='w', width=output_variables_width)
        label_1_1.grid(column=1, row=1)

        label_1_2 = Label(output_frame, textvariable=gene_location_str, anchor='w', width=output_variables_width)
        label_1_2.grid(column=1, row=2)

        label_1_3 = Label(output_frame, textvariable=gene_class_str, anchor='w', width=output_variables_width)
        label_1_3.grid(column=1, row=3)

        label_1_4 = Label(output_frame, textvariable=go_term_str, anchor='w', width=output_variables_width)
        label_1_4.grid(column=1, row=4)

        label_1_5 = Label(output_frame, textvariable=pfam_id_str, anchor='w', width=output_variables_width)
        label_1_5.grid(column=1, row=5)

        label_1_6 = Label(output_frame, textvariable=interpro_id_str, anchor='w', width=output_variables_width)
        label_1_6.grid(column=1, row=6)

    except Exception:
        pass


def button_press(*args):
    if source_selected.get() == 1:
        try:
            barlex_data()
        except Exception:
            pass
    if source_selected.get() == 2:
        try:
            ensembl_api()
        except Exception:
            pass


def ensembl_api(*args):
    try:
        # Setup for Ensembl REST API single entry lookup
        server = "https://rest.ensembl.org"
        ext = "/lookup/id/"
        headers = {"Content-Type": "application/json"}

        # Define URL for GET request
        url = server + ext + gene_id.get()

        # GET the information request
        ensembl_response = requests.get(url, headers=headers)

        # Unpack the returned JSON response
        ensembl_json = ensembl_response.json()

        # Extract the gene annotation
        ensembl_annotation = re.sub(r'\s*\[.*\]', '', ensembl_json.get('description'))

        ensembl_annotation_str = StringVar()
        ensembl_annotation_str.set(ensembl_annotation)

        # Clear global variables for outputs
        output_frame_clear()

        # Pull in output frame variables from global env
        global output_frame

        global label_0_0
        global label_0_1
        global label_0_2
        global label_0_3
        global label_0_4
        global label_0_5
        global label_0_6

        global label_1_0
        global label_1_1
        global label_1_2
        global label_1_3
        global label_1_4
        global label_1_5
        global label_1_6

        # Display outputs
        output_labels_width = 20
        output_variables_width = 50

        label_0_0 = Label(output_frame, text='Ensembl Annotation:', anchor='e', width=output_labels_width)
        label_0_0.grid(column=0, row=0)

        label_1_0 = Label(output_frame, textvariable=ensembl_annotation_str, anchor='w', width=output_variables_width)
        label_1_0.grid(column=1, row=0)

    except Exception:
        pass


def output_frame_clear(*args):
    # Set up global variables for outputs
    global output_frame

    global label_0_0
    global label_0_1
    global label_0_2
    global label_0_3
    global label_0_4
    global label_0_5
    global label_0_6

    global label_1_0
    global label_1_1
    global label_1_2
    global label_1_3
    global label_1_4
    global label_1_5
    global label_1_6

    label_0_0.grid_forget()
    label_0_1.grid_forget()
    label_0_2.grid_forget()
    label_0_3.grid_forget()
    label_0_4.grid_forget()
    label_0_5.grid_forget()
    label_0_6.grid_forget()

    label_1_0.grid_forget()
    label_1_1.grid_forget()
    label_1_2.grid_forget()
    label_1_3.grid_forget()
    label_1_4.grid_forget()
    label_1_5.grid_forget()
    label_1_6.grid_forget()


# Import preprocessed BARLEX data from 'barlex_df.csv'
barlex_df = pd.read_csv('data/barlex_df.csv', index_col='gene_id')

# Clean id strings into lists of ids
cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
for col in cols_to_list:
    barlex_df[col] = barlex_df[col].str.split(pat=', ').tolist()

# Establish main window
window = Tk()
window.title("EnsemblX")

# Create title
title_frame = Frame(window)
title_frame.grid(row=0, column=0)

title_quick = Label(title_frame, text="Quick Reference", font=('Arial', 20), padx=100)
title_quick.grid(column=0, row=0)

# Initialize variables
gene_id = StringVar()

# Clear and reform frame
output_frame = Frame(window)
output_frame.grid(column=0, row=3)

# Create input interactions
entry_frame = Frame(window)
entry_frame.grid(column=0, row=1)

entry_label = Label(entry_frame, text="Enter Gene ID:", padx=10, font=('Arial', 16))
entry_label.grid(column=0, row=0)

entry_box = Entry(entry_frame, width=20, textvariable=gene_id)
entry_box.grid(column=1, row=0)

entry_button = Button(entry_frame, text="Go", command=button_press, padx=10)
entry_button.grid(column=2, row=0)

# Create output source selector
source_select_frame = Frame(window)
source_select_frame.grid(column=0, row=2)

source_selected = IntVar()
source_selected.set(1)

source_select_barlex = Radiobutton(source_select_frame, text='BARLEX: CDS HC May 2016', value=1,
                                   variable=source_selected)
source_select_barlex.grid(column=0, row=0)

source_select_ensembl = Radiobutton(source_select_frame, text='Ensembl API', value=2, variable=source_selected)
source_select_ensembl.grid(column=1, row=0)

# Create output frame
output_frame = Frame(window)
output_frame.grid(column=0, row=3)

label_0_0 = Label()
label_0_1 = Label()
label_0_2 = Label()
label_0_3 = Label()
label_0_4 = Label()
label_0_5 = Label()
label_0_6 = Label()

label_1_0 = Label()
label_1_1 = Label()
label_1_2 = Label()
label_1_3 = Label()
label_1_4 = Label()
label_1_5 = Label()
label_1_6 = Label()

window.mainloop()
