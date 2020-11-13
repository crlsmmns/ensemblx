# EnsemblX

:warning: **CAUTION**: The v1.0.0-pre2.0.0 release of EnsemblX in this repository is a retired, R-based web scraping script. I am in the process of creating v2.0.0 which will change EnsemblX to being Python-based and transition the retrieval of the required data away from web scraping and towards APIs and downloadable datasets (in CSV files).

My original EnsemblX script was created very early in my programming journey and as such tried to respect the general terms of use for each website but failed to recognized that web scraper etiquette was instead encoded on the websites' `robots.txt` files. Thus, it became clear that the gene annotation information had to be retrieved by other means in order to respect both websites' scraper etiquette.

This means that in EnsemblX v2.0.0 the Ensembl Plants data will be retrieved using the Ensembl REST API [POST lookup/id ](https://rest.ensembl.org/documentation/info/lookup_post) functionality and that the BARLEX data will be retrieved from the `160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta.gz` dataset available from the downloads page of the BARLEX BLAST server found [here](https://webblast.ipk-gatersleben.de/barley_ibsc/downloads/).

Thus far, in preliminary tests, switching to these data retrieval methods has resulted in an increase in speed and efficiency especially when conducting high-throughput referencing of gene entries related to transcriptomic datasets.

## Description

EnsemblX is a niche, but potentially useful, Python script for automating the retrieval of short gene descriptions (and some of the relevant metadata) for barley genes using Gene Stable IDs to reference the matching gene entries from [Ensembl Plants](https://plants.ensembl.org/) and [BARLEX](http://barlex.barleysequence.org/).

This script was created to facilitate the typically manual process of copying and pasting the relevant information required to retrieve gene descriptions for select genes of interest through each genome browser's website interface.

Currently, the main functionality of reading and writing the proper information to and from a multi-sheet Excel file is still being coded; however, the base retrieval functions have been coded into a simple, proof-of-concept GUI as a "Quick Reference" widget.

Below is a GIF demonstration of that functionality whereby the VRN-H1 [example gene entry](https://plants.ensembl.org/Hordeum_vulgare/Gene/Summary?g=HORVU5Hr1G095630) from Ensembl Plants is referenced using its Gene Stable ID: HORVU5Hr1G095630. This widget is not currently packaged as an executable but can be run via the `ensemblx.py` script.

![Quick Reference Animated Demo](https://github.com/crlsmmns/ensemblx/blob/main/quick_reference_demo.gif)
