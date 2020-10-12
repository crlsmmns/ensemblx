# EnsemblX

:warning: **CAUTION**: Do not use EnsemblX in its current state on this repository. This repository is being used for change tracking and project backups as I try to transition this script away from using web scraping and towards using APIs. My original EnsemblX script was created very early in my programming journey and as such tried to respect the general terms of use for each website but failed to recognized that web scraping etiquette was instead encoded on the websites' `robots.txt` files. Thus, it has become clear that the gene annotation information has to be retrieved by other means in order to respect both websites' etiquette. Currently, this means that I am transitioning to [Ensembl REST API Endpoints](https://rest.ensembl.org/) and trying to find an alternative solution to access the gene annotation information from BARLEX.

## Description

EnsemblX is a niche, but potentially useful, R script for automating the retrieval of short gene descriptions for barley genes using Gene Stable IDs to reference the matching gene entries from [BARLEX](http://barlex.barleysequence.org/) and [Ensembl Plants](https://plants.ensembl.org/) simultaneously.

This script was created to facilitate the typically manual process of copying and pasting the relevant information required to retrieve gene descriptions for select genes of interest through each genome browser's website interface.

Thus far, the most common use case has been batches of a few hundred genes at a time (usually 200~300 genes) which typically completes in under an hour. The script is a bit slow but less tedious than completing the process by hand.