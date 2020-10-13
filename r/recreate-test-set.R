#This R script will recreate the test set of genes used to test the
#functionality of the main ensemblx.R script

#Attach required packages
library(tibble)
library(writexl)

#Create table with example barley alpha amylase genes
test_alpha_amylases <- tibble(
  gene_id = c(
    "HORVU5Hr1G068350",
    "HORVU5Hr1G068350",
    "HORVU3Hr1G067620",
    "HORVU3Hr1G067620",
    "HORVU7Hr1G091150"
  ),
  barlex_desc = rep(NA, times = 5),
  ensembl_desc = rep(NA, times = 5)
)

#Create table with example barley beta amylase genes
test_beta_amylases <- tibble(
  gene_id = c(
    "HORVU2Hr1G020970",
    "HORVU2Hr1G020970",
    "HORVU6Hr1G015670",
    "HORVU6Hr1G015670",
    "HORVU4Hr1G000520"
  ),
  barlex_desc = rep(NA, times = 5),
  ensembl_desc = rep(NA, times = 5)
)

#Create a list containing the two tables
test_set <- list(test_alpha_amylases, test_beta_amylases)
names(test_set) <- c("test_alpha_amylases", "test_beta_amylases")

#Write list of tables to Excel document to recreate test-set.xlsx in the input
#directory
write_xlsx(test_set, path = "input/test-set.xlsx")