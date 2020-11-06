# EnsemblX

:warning: **CAUTION**: The v1.0.0 release of EnsemblX is an R-based web scraping script. I am in the process of creating v2.0.0 which will change EnsemblX to being Python-based and transition the retrieval of the required data away from web scraping and towards APIs and downloadable datasets (in CSV files).

My original EnsemblX script was created very early in my programming journey and as such tried to respect the general terms of use for each website but failed to recognized that web scraper etiquette was instead encoded on the websites' `robots.txt` files. Thus, it became clear that the gene annotation information had to be retrieved by other means in order to respect both websites' scraper etiquette.

This will mean that in EnsemblX v2.0.0 the Ensembl Plants data will be retrieved using the Ensembl REST API [POST lookup/id ](https://rest.ensembl.org/documentation/info/lookup_post) functionality and that the BARLEX data will be retrieved from the `160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta.gz` dataset available from the downloads page of the BARLEX BLAST server found [here](https://webblast.ipk-gatersleben.de/barley_ibsc/downloads/). These changes will also likely increase the number of Gene Stable IDs that can be processed effectively by reducing the request times for both the Ensembl Plants and BARLEX data.

## Description

EnsemblX is a niche, but potentially useful, R script for automating the retrieval of short gene descriptions for barley genes using Gene Stable IDs to reference the matching gene entries from [BARLEX](http://barlex.barleysequence.org/) and [Ensembl Plants](https://plants.ensembl.org/) simultaneously.

This script was created to facilitate the typically manual process of copying and pasting the relevant information required to retrieve gene descriptions for select genes of interest through each genome browser's website interface.

Thus far, the most common use case has been batches of a few hundred genes at a time (usually 200~300 genes) which typically completes in under an hour. The script is a bit slow but less tedious than completing the process by hand.