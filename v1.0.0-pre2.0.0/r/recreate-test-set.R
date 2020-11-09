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