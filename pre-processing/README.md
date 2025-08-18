# Data Preparation and Pre-processing:

This folder contains all R and Python files used to pre-process the datasets used for analysis in this dissertation project. These include:

1. combining_990_eobmf.R: The R file used to 1) clean and combine 990 and 990-EZ datasets from each year (2013 to 2020), 2) clean and combine all historical EO-BMF datasets, including de-duplication, and 3) merge these 990 datasets with EO-BMF data, bringing together organization-year level data containing Employer Identification numbers with organization-year level data containing addresses.

2. geocoding.py: The Python file used to geocode all 990 return .csvs that contain organization-year level financial return data and address data.
