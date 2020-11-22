################################################################################
# EnsemblX automates the retrieval of short gene descriptions for barley genes.
#### Copyright (C) 2020  Carl H. Simmons
################################################################################
#### This program is free software: you can redistribute it and/or modify it
#### under the terms of the GNU General Public License as published by the Free
#### Software Foundation, either version 3 of the License, or (at your option)
#### any later version.
################################################################################
#### This program is distributed in the hope that it will be useful, but
#### WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#### or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
#### License for more details.
################################################################################
#### You should have received a copy of the GNU General Public License along
#### with this program. If not, see <https://www.gnu.org/licenses/>.
################################################################################

import numpy as np
import pandas as pd


def barlex_data(file_path):
    with open(file_path, 'r') as barlex_file:
        barlex_headers = []
        for line in barlex_file:
            if line.startswith('>'):
                barlex_headers.append(line[1:])

    barlex_headers = np.array(barlex_headers).reshape((-1, 1))
    barlex_df = pd.DataFrame(barlex_headers, columns=['import_str'])
    barlex_df = barlex_df['import_str'].str.split(pat='|', expand=True)

    barlex_df.columns = [
        'gene_id',
        'gene_location',
        'gene_class',
        'barlex_annotation',
        'go_terms',
        'pfam_id',
        'interpro_id'
    ]

    barlex_df[['gene_transcript_id', 'gene_id']] = barlex_df['gene_id'].str.split(pat='\t', expand=True)

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

    barlex_df['interpro_id'] = barlex_df['interpro_id'].str.replace('\n', '')

    gene_class_dict = {
        'HC_G': 'high-confidence gene with predicted function due to homology to a reference protein',
        'HC_U': 'high-confidence gene with homology to a reference protein but with unknown predicted function',
        'HC_u': 'high-confidence gene with homology to a reference protein but without a predicted function',
        'HC_TE?': 'high-confidence gene with homology to a reference protein, but a potential transposable element'
    }
    barlex_df['gene_class'] = barlex_df['gene_class'].map(gene_class_dict)

    barlex_df.set_index('gene_id', inplace=True)

    return barlex_df


barlex_clean_df = barlex_data('data/160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta')
barlex_clean_df.to_csv('data/barlex_clean_df.csv')
