# EnsemblX

### Description

EnsemblX is a niche, but useful, Python project that seeks to speed up and simplify the retrieval of short gene descriptions (and other relevant data) for barley genes using their Gene Stable IDs to reference the matching annotations from [Ensembl Plants](https://plants.ensembl.org/) and [BARLEX](http://barlex.barleysequence.org/).

### Origin

In its first form, EnsemblX was an R script that used web scraping to pull down the annotation information from each genome browser's web interface; however, as EnsemblX progressed (and I personally learned more about programming and web scraping) it became apparent that web scraping was slow and disallowed on the specific pages the R script scraped.

### v2.0.0
In the Python-based EnsemblX v2.0.0, the Ensembl Plants data is now retrieved using the Ensembl REST API [POST lookup/id ](https://rest.ensembl.org/documentation/info/lookup_post) functionality and the BARLEX data is referenced from a local, pre-processed copy of the data retrieved as the `160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta.gz` dataset (available [here](https://webblast.ipk-gatersleben.de/barley_ibsc/downloads/)).

EnsemblX was originally created to facilitate the typically repetative, manual process of copying and pasting the relevant information for select genes of interest through each genome browser's website interface. As such, EnsemblX v2.0.0 tries to simplify the process even further by providing a basic user interface to interact with the annotation workflow. This user interface is currently built using Tkinter with ttk widgets for an native style across operating systems (currently tested on Windows 10 and macOS Catalina). 

&nbsp; | Windows 10 | macOS Catalina
:------|:-------------------------:|:-------------------------:
Start Page|![]('ensemblx_startpage_windows10.png')  |  ![]('ensemblx_startpage_macoscatalina.png')
Excel Page|![]('ensemblx_startpage_windows10.png')  |  ![]('ensemblx_startpage_macoscatalina.png')

### Future Updates



Currently, the main functionality of reading and writing the proper information to and from a multi-sheet Excel file has been coded in v2.0.0. This feature is 

Below is a GIF demonstration of that functionality whereby the VRN-H1 [example gene entry](https://plants.ensembl.org/Hordeum_vulgare/Gene/Summary?g=HORVU5Hr1G095630) from Ensembl Plants is referenced using its Gene Stable ID: HORVU5Hr1G095630. This widget is not currently packaged as an executable but can be run via the `ensemblx.py` script.
