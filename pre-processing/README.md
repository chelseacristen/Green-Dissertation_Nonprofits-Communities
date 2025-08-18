# Data Preparation and Pre-processing:

This folder contains all R and Python files used to pre-process the datasets used for analysis in this dissertation project. These include:

1: **step_1_creating_full_eobmf.R:** Created to process NCCS and NBER historical EO-BMF data files, clean them, create subsets, deduplicate them, and merge them together. 

2: **step_2_combining_990_eobmf.R:** Created to 1) clean and combine 990 and 990-EZ datasets from each year (2013 to 2020), 2) clean and combine all historical EO-BMF datasets, including de-duplication, and 3) merge these 990 datasets with EO-BMF data, bringing together organization-year level data containing Employer Identification numbers with organization-year level data containing addresses.

3.**step_3_geocoding.py:** Created to geocode all 990 return .csvs that contain organization-year level financial return data and address data.
4. **scraping_990s.py:** Created to scrape all publicly available 990 tax return PDFs and output organization-year level datasets containing information on how much an organization reported receiving that tax year in government grant contributions. (Because these were computationally expensive to scrape, I wrote the script to create a dataset associated with each respective IRS tax filing year. These datasets were then combined to create a 2016-2022 organization-year level dataset on government grant contributions received).
