#This is the main R script for EnsemblX. Running this script will pull
#information stored in the input Excel file, try to retrieve gene descriptions
#for each gene from BARLEX and Ensembl Plants, and then write the information
#into a new Excel file. The final Excel file should preserve the original sheets
#and sheet names so that genes can be subsetted into groups before processing.

#Set path_to_file variable to the input Excel file path
path_to_file <- as.character("input/test-set.xlsx")

#Attach required packages
library(data.table)
library(dplyr)
library(readxl)
library(rvest)
library(stringr)
library(writexl)

#Define web scraping functions
##Function for Barlex website
get_barlex_desc <- function(gene_id) {
  #Assemble full URL from the URL_stem and gene_id variables
  URL_stem <-
    "https://apex.ipk-gatersleben.de/apex/f?p=284:45:::NO::P45_GENE_NAME:"
  assembled_URL <- url(paste0(URL_stem, gene_id))
  
  #Retrieve HTML table from Barlex website containing the gene description
  barlex_info_table <- assembled_URL %>%
    read_html() %>%
    html_nodes(xpath = '//*[@id="R91876968009274642"]/div[2]/table') %>%
    html_table()
  
  #Extract the description string from table
  barlex_annotation <- barlex_info_table[[1]][4, 2]
  
  #Split off the simple gene description from full string
  barlex_annotation_vector <-
    str_split(string = barlex_annotation, pattern = "\\|")
  barlex_desc <- barlex_annotation_vector[[1]][4]
  
  #Return only the simple gene description
  return(barlex_desc)
}

##Function for Ensembl Plants website
get_ensembl_desc <- function(gene_id) {
  #Assemble full URL from the URL_stem and gene_id variables
  URL_stem <-
    "https://plants.ensembl.org/Multi/Search/Results?species=all;idx=;q="
  assembled_URL <- url(paste0(URL_stem, gene_id))
  
  #Retrieve HTML from Ensembl Plants website containing the gene description
  ensemble_full_desc <- assembled_URL %>%
    read_html() %>%
    html_nodes('p') %>%
    xml_find_all("//div[contains(@class, 'rhs')]") %>%
    html_text()
  
  #Split off the simple gene description from full string
  ensemble_desc <-
    str_remove(string = ensemble_full_desc[1], pattern = " \\[Source:.*\\]")
  
  #Return only the simple gene description
  return(ensemble_desc)
}

#Read in all sheets from Excel workbook
sheets <- excel_sheets(path_to_file)
list_of_tables <- lapply(sheets, read_xlsx, path = path_to_file)
names(list_of_tables) <- sheets

#Sanity check of data format
##Remove rows missing a Gene Stable ID
list_of_tables <- lapply(list_of_tables, filter, !is.na(gene_id))

##Remove rows with any repeats of the header within the data
list_of_tables <- lapply(list_of_tables, filter, gene_id != "gene_id")

#Unify list of tables into a single iterable data frame with ID column for
#seperation back into original Excel sheets upon export
unified_table <- rbindlist(list_of_tables, idcol = TRUE)

#Record number of entries to iterate through
num_entries <- nrow(unified_table)

#Run a for loop that attempts to retrieve and write the Barlex description for
#each entry
for (i in 1:num_entries) {
  #Try description grab
  try(unified_table$barlex_desc[i] <-
        get_barlex_desc(unified_table$gene_id[i]))
  
  #Print a progress report after each interation
  print(paste0(
    "Completed Barlex Grab (",
    as.character(i),
    "/",
    as.character(num_entries),
    ")"
  ))
}

#Run a for loop that attempts to retrieve and write the Ensembl Plants
#description for each entry
for (i in 1:num_entries) {
  #Try description grab
  try(unified_table$ensembl_desc[i] <-
        get_ensembl_desc(unified_table$gene_id[i]))
  
  #Print a progress report after each interation
  print(paste0(
    "Completed Ensembl Grab (",
    as.character(i),
    "/",
    as.character(num_entries),
    ")"
  ))
}

#Split the unified data frame back into a list of sheets
output_split <- unified_table %>% group_split(.id, .keep = FALSE)

#Sort original sheet name vector alphabetically to match the alphabetically
#organize list of tables post-split
sorted_sheets <- sort(sheets)
names(output_split) <- sorted_sheets

#Create file path for the output that appends the "-output" tag to the original
#file name and places the output in the same directory as the original file
file_name <- str_match(path_to_file, pattern = "\\/(.+)\\.xlsx$")
output_file <- paste0("output/", file_name[1, 2], "-output.xlsx")

#Write tables to Excel file
write_xlsx(output_split, path = output_file)