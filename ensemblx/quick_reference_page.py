import tkinter as tk
from tkinter import ttk

import pandas as pd
import requests
import re

import ensemblx.start_page as start_page


class QuickReferencePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        s = ttk.Style()
        s.configure('Title.TLabel', font=('Arial', 24))
        s.configure('EntryLabel.TLabel', font=('Arial', 16), padding=[0, 0, 5, 0])
        s.configure('EntryBox.TEntry', font=('Arial', 16))
        s.configure('EntryButton.TButton', font=('Arial', 12))

        frame1 = tk.Frame(self)
        frame1.pack(pady=10)

        title = ttk.Label(frame1, text="Quick Reference", style='Title.TLabel')
        title.pack()

        gene_id = tk.StringVar()

        frame2 = tk.Frame(self)
        frame2.pack()

        entry_label = ttk.Label(frame2, text="Enter Gene ID:", style='EntryLabel.TLabel')
        entry_label.pack(side='left')

        entry_box = ttk.Entry(frame2, width=20, textvariable=gene_id)
        entry_box.pack(side='left')

        entry_button = ttk.Button(frame2, text="Go", command=lambda: self.ensembl_output(gene_id))
        entry_button.pack(side='left', padx=10)

        self.frame3 = tk.Frame(self)
        self.frame3.pack(padx=10, pady=10)

        self.ensembl_frame_gene_annotation = tk.Frame(self.frame3)
        self.ensembl_frame_gene_annotation.pack()

        self.ensembl_gene_annotation_label = ttk.Label(self.ensembl_frame_gene_annotation)
        self.ensembl_gene_annotation_label.pack(side='left')

        self.ensembl_gene_annotation = ttk.Label(self.ensembl_frame_gene_annotation)
        self.ensembl_gene_annotation.pack(side='left')

        self.barlex_frame_gene_annotation = tk.Frame(self.frame3)
        self.barlex_frame_gene_annotation.pack()

        self.gene_annotation_label = ttk.Label(self.barlex_frame_gene_annotation)
        self.gene_annotation_label.pack(side='left')

        self.gene_annotation = ttk.Label(self.barlex_frame_gene_annotation)
        self.gene_annotation.pack(side='left')

        frame_gene_transcript = tk.Frame(self.frame3)
        frame_gene_transcript.pack()

        self.gene_transcript_label = ttk.Label(frame_gene_transcript)
        self.gene_transcript_label.pack(side='left')

        self.gene_transcript = ttk.Label(frame_gene_transcript)
        self.gene_transcript.pack(side='left')

        frame_gene_location = tk.Frame(self.frame3)
        frame_gene_location.pack()

        self.gene_location_label = ttk.Label(frame_gene_location)
        self.gene_location_label.pack(side='left')

        self.gene_location = ttk.Label(frame_gene_location)
        self.gene_location.pack(side='left')

        frame_gene_class = tk.Frame(self.frame3)
        frame_gene_class.pack()

        self.gene_class_label = ttk.Label(frame_gene_class)
        self.gene_class_label.pack(side='left')

        self.gene_class = ttk.Label(frame_gene_class)
        self.gene_class.pack(side='left')

        frame_go_terms = tk.Frame(self.frame3)
        frame_go_terms.pack()

        self.go_terms_label = ttk.Label(frame_go_terms)
        self.go_terms_label.pack(side='left')

        self.go_terms = ttk.Label(frame_go_terms)
        self.go_terms.pack(side='left')

        frame_pfam_ids = tk.Frame(self.frame3)
        frame_pfam_ids.pack()

        self.pfam_ids_label = ttk.Label(frame_pfam_ids)
        self.pfam_ids_label.pack(side='left')

        self.pfam_ids = ttk.Label(frame_pfam_ids)
        self.pfam_ids.pack(side='left')

        frame_interpro_ids = tk.Frame(self.frame3)
        frame_interpro_ids.pack()

        self.interpro_ids_label = ttk.Label(frame_interpro_ids)
        self.interpro_ids_label.pack(side='left')

        self.interpro_ids = ttk.Label(frame_interpro_ids)
        self.interpro_ids.pack(side='left')

        frame4 = tk.Frame(self)
        frame4.pack(padx=10, pady=10)

        return_button = ttk.Button(frame4, text="Return to Start Page",
                                   command=lambda: controller.show_frame(start_page.StartPage))
        return_button.pack()

        self.barlex_df = pd.read_csv('data/barlex_clean_df.csv', index_col='gene_id')

        cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
        for col in cols_to_list:
            self.barlex_df[col] = self.barlex_df[col].str.split(pat=', ').tolist()

    def barlex_output(self, gene_id):
        try:
            barlex_entry = self.barlex_df.loc[gene_id.get()]

            barlex_gene_annotation_str = tk.StringVar()
            barlex_gene_transcript_str = tk.StringVar()
            barlex_gene_location_str = tk.StringVar()
            barlex_gene_class_str = tk.StringVar()
            barlex_go_term_str = tk.StringVar()
            barlex_pfam_ids_str = tk.StringVar()
            barlex_interpro_ids_str = tk.StringVar()

            barlex_annotation = barlex_entry['barlex_annotation']
            barlex_gene_annotation_str.set(barlex_annotation)

            gene_transcript_id = barlex_entry['gene_transcript_id']
            barlex_gene_transcript_str.set(gene_transcript_id)

            gene_location = barlex_entry['gene_location']
            barlex_gene_location_str.set(gene_location)

            gene_class = barlex_entry['gene_class']
            barlex_gene_class_str.set(gene_class)

            go_term_list = barlex_entry['go_terms']
            barlex_go_term_str.set(", ".join(go_term_list))

            pfam_ids_list = barlex_entry['pfam_id']
            barlex_pfam_ids_str.set(", ".join(pfam_ids_list))

            interpro_ids_list = barlex_entry['interpro_id']
            barlex_interpro_ids_str.set(", ".join(interpro_ids_list))

            self.frame_gene_annotation.config(highlightbackground="black", highlightthickness=0)
            self.frame4.config(highlightbackground="black", highlightthickness=1)

            self.gene_annotation_label.config(text='Annotation:', font=('Arial', 10, 'bold'))
            self.gene_annotation.config(text=gene_annotation_str.get(), font=('Arial', 10, 'italic'))

            self.gene_transcript_label.config(text='Transcript ID:', font=('Arial', 10, 'bold'))
            self.gene_transcript.config(text=gene_transcript_str.get(), font=('Arial', 10, 'italic'))

            self.gene_location_label.config(text='Location:', font=('Arial', 10, 'bold'))
            self.gene_location.config(text=gene_location_str.get(), font=('Arial', 10, 'italic'))

            self.gene_class_label.config(text='Class:', font=('Arial', 10, 'bold'))
            self.gene_class.config(text=gene_class_str.get(), font=('Arial', 10, 'italic'))

            self.go_terms_label.config(text='GO Terms:', font=('Arial', 10, 'bold'))
            self.go_terms.config(text=go_term_str.get(), font=('Arial', 10, 'italic'))

            self.pfam_ids_label.config(text='Pfam Protein Families:', font=('Arial', 10, 'bold'))
            self.pfam_ids.config(text=pfam_ids_str.get(), font=('Arial', 10, 'italic'))

            self.interpro_ids_label.config(text='InterPro Protein Families:', font=('Arial', 10, 'bold'))
            self.interpro_ids.config(text=interpro_ids_str.get(), font=('Arial', 10, 'italic'))
        except KeyError:
            self.frame3.config(highlightbackground="black", highlightthickness=0)
            self.frame_gene_annotation.config(highlightbackground="black", highlightthickness=1)

            self.gene_annotation_label.config(text='BARLEX Entry:', font=('Arial', 10, 'bold'))
            self.gene_annotation.config(text='Not Found', font=('Arial', 10, 'italic'))

            self.gene_transcript_label.config(text='')
            self.gene_transcript.config(text='')

            self.gene_location_label.config(text='')
            self.gene_location.config(text='')

            self.gene_class_label.config(text='')
            self.gene_class.config(text='')

            self.go_terms_label.config(text='')
            self.go_terms.config(text='')

            self.pfam_ids_label.config(text='')
            self.pfam_ids.config(text='')

            self.interpro_ids_label.config(text='')
            self.interpro_ids.config(text='')

    def ensembl_output(self, gene_id):
        server = "https://rest.ensembl.org"
        ext = "/lookup/id/"
        headers = {"Content-Type": "application/json"}

        url = server + ext + gene_id.get()

        ensembl_response = requests.get(url, headers=headers)

        ensembl_json = ensembl_response.json()

        ensembl_annotation = re.sub(r'\s*\[.*\]', '', ensembl_json.get('description'))
        ensembl_source = re.search(r'\[.*\]', ensembl_json.get('description')).group(0)
        ensembl_source = re.sub(r'\[\w*\:|]', '', ensembl_source)
        ensembl_source = ensembl_source.strip()
        ensembl_gene_name = ensembl_json.get('display_name')
        ensembl_location = ensembl_json.get('seq_region_name') + ':' + str(ensembl_json.get('start')) + '-' + str(ensembl_json.get('end'))

        if ensembl_json.get('display_name') is not None:
            self.ensembl_gene_annotation_label.config(text='Gene Name:', font=('Arial', 10, 'bold'))
            self.ensembl_gene_annotation.config(text=ensembl_annotation, font=('Arial', 10, 'italic'))
        else:
            self.gene_annotation_label.config(text='')
            self.gene_annotation.config(text='')

        if ensembl_json.get('display_name') is not None:
            self.ensembl_gene_annotation_label.config(text='Gene Name:', font=('Arial', 10, 'bold'))
            self.ensembl_gene_annotation.config(text=ensembl_gene_name, font=('Arial', 10, 'italic'))
        else:
            self.gene_annotation_label.config(text='')
            self.gene_annotation.config(text='')
