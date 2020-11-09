import numpy as np
import pandas as pd


def barlex_data(file_path):
    # Read in FASTA sequence headers marked with '>' but do not read in DNA sequences
    with open(file_path, 'r') as barlex_file:
        barlex_headers = []
        for line in barlex_file:
            if line.startswith('>'):
                barlex_headers.append(line[1:])

    # Separate individual fields of data from the sequence headers
    barlex_headers = np.array(barlex_headers).reshape((-1, 1))
    barlex_df = pd.DataFrame(barlex_headers, columns=['import_str'])
    barlex_df = barlex_df['import_str'].str.split(pat='|', expand=True)

    # Label the new columns appropriately
    barlex_df.columns = [
        'gene_id',
        'gene_location',
        'gene_class',
        'barlex_annotation',
        'go_terms',
        'pfam_id',
        'interpro_id'
    ]

    # Split gene ids from the gene ids with transcript identifier
    barlex_df[['gene_transcript_id', 'gene_id']] = barlex_df['gene_id'].str.split(pat='\t', expand=True)

    # Reorder DataFrame columns
    barlex_df = barlex_df[[
        'gene_id',
        'gene_transcript_id',
        'gene_location',
        'gene_class',
        'barlex_annotation',
        'go_terms',
        'pfam_id',
        'interpro_id'
    ]]

    # Remove errant line breaks in the InterPro Ids
    barlex_df['interpro_id'] = barlex_df['interpro_id'].str.replace('\n', '')

    # Clean id strings into lists of ids
    cols_to_list = ['go_terms', 'pfam_id', 'interpro_id']
    for col in cols_to_list:
        barlex_df[col] = barlex_df[col].str.split(pat=', ').tolist()

    # Recode gene classes from abbreviations to descriptive strings
    gene_class_dict = {
        'HC_G': 'high-confidence gene with predicted function due to homology to a reference protein',
        'HC_U': 'high-confidence gene with homology to a reference protein but with unknown predicted function',
        'HC_u': 'high-confidence gene with homology to a reference protein but without a predicted function',
        'HC_TE?': 'high-confidence gene with homology to a reference protein, but a potential transposable element'
    }
    barlex_df['gene_class'] = barlex_df['gene_class'].map(gene_class_dict)

    # Set index of DataFrame to gene ids
    barlex_df.set_index('gene_id', inplace=True)

    # Return the clean DataFrame
    return barlex_df


# Pre-process and save
barlex_df = barlex_data('../data/160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta')
barlex_df.to_csv('../data/barlex_df.csv')
