# EnsemblX

### Description

EnsemblX is a niche, but potentially useful, Python applet that seeks to speed up and simplify the retrieval of short gene descriptions (and other relevant data) for barley genes using their Gene Stable IDs to reference the matching annotations from [Ensembl Plants](https://plants.ensembl.org/) and [BARLEX](http://barlex.barleysequence.org/). EnsemblX is a free-time endeavor used mainly as a hands-on project to encapsulate my experimentation with applying programming to biological data handling as I learn Python.

### Getting Started

To learn how to download and use EnsemblX visit the wiki [here](https://github.com/crlsmmns/ensemblx/wiki) on GitHub.

### Origin

In its first form, EnsemblX was an R script (here tagged as v1.0.0-pre2.0.0) that used web scraping to pull down the annotation information from each genome browser's web interface; however, as EnsemblX progressed (and I progressed in my programming knowledge) it became apparent that web scraping was slow and discouraged on the specific pages the R script scraped. Therefore an alternative data retrieval method was necessary.

### v2.0.0
In the Python-based EnsemblX v2.0.0, the Ensembl Plants data is now retrieved using the Ensembl REST API [POST lookup/id ](https://rest.ensembl.org/documentation/info/lookup_post) functionality and the BARLEX data is referenced from a local, pre-processed copy of the data retrieved as the `160517_Hv_IBSC_PGSB_r1_CDS_HighConf_REPR_annotation.fasta.gz` dataset (available [here](https://webblast.ipk-gatersleben.de/barley_ibsc/downloads/)). The code for pre-processing this data can be found in the `data_pre_processing.py` Python script.

EnsemblX was created to facilitate the typically repetitive, manual process of copying and pasting the relevant information for select genes of interest through each genome browser's web interface. As such, EnsemblX v2.0.0 tries to simplify the process even further by providing a basic user interface to interact with the underlying workflow. This user interface is currently built using tkinter with ttk widgets and the workflow relies on pandas to manage and manipulate the incoming and outgoing data.

Below are screenshots of the two main GUI pages implemented in EnsemblX v2.0.0. The start page is the opening page of the applet that links to the other GUI pages (in v2.0.0 the Excel page and a disabled button for a future quick reference page). The start page also provides easy reference within the GUI to the GitHub wiki and repository.

Start Page|Excel Page
:---:|:---:
![Windows 10 Start Page](https://github.com/crlsmmns/ensemblx/blob/v2.0.0/images/ensemblx_startpage_windows10.png) | ![Windows 10 Excel Page](https://github.com/crlsmmns/ensemblx/blob/v2.0.0/images/ensemblx_excelpage_windows10.png)

### Current Bugs for Future Versions
* The process for creating the executable version of EnsemblX with pyinstaller currently only works for creating the Windows executable. Trial and error has not yet led to a functioning macOS application.
* While the underlying workflow is running, the GUI often becomes unresponsive until the process is complete. The solution may involve running the underlying workflow in a separate processing thread so that the tkinter `mainloop()` is always free to update the GUI widgets.
* The first implementation of the quick reference feature (currently removed except for a disabled placeholder button on the start page of the GUI) could not be formatted properly using my current understanding of tkinter and the ttk widgets. Perhaps creating and destroying frames and widgets as needed with the `destroy()` method (as opposed to stacking and raising them with the `show_frame()` method) would better support displaying the varying format of the quick reference output on-screen.
* There is no option for selecting which data fields to return from each source in the final output so the final Excel file contains all the information returned from the selected source(s). Implementing a hierarchical list of the data fields available from each source (with checkboxes to select them) could be used to generate a string of the desired data fields by which to filter the final pandas DataFrame before writing to Excel.
* The "File Selected" text on the Excel page retains the originally selected file if the open file window is opened and closed without selecting a new file.