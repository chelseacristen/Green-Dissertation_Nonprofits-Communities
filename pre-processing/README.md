# Data Preparation and Pre-processing:

This folder contains the data engineering infrastructure developed to tackle the complex integration challenges of federal nonprofit datasets. These automated workflows transform disparate data sources—including multi-format IRS filings, geographic boundaries, and organizational records spanning over a decade—into analysis-ready research data through schema harmonization, large-scale OCR processing, and geospatial data integration across millions of organizational records. These foundational datasets power the analysis presented in this dissertation.

1: **NCCS-NBER Nonprofit Data Processing Pipeline (nccs_nber_data_processing.R):** Comprehensive R-based data processing pipeline that standardizes, cleans, and merges nonprofit organizational data from National Center for Charitable Statistics (NCCS) and National Bureau of Economic Research (NBER) sources. The script harmonizes disparate data schemas, creates state-year subsets, performs multi-level deduplication, and generates analysis-ready datasets for longitudinal nonprofit research. 

*Dependencies: dplyr, stringr, data.table, qpcR
Data Sources: NCCS Core Files, NBER EO-BMF extracts*

2: **IRS Tax-Exempt Organization Data Integration Pipeline (irs_data_integration.R):** Multi-source data integration system that processes and harmonizes IRS tax-exempt organization datasets, including Form 990, 990-EZ filings, Publication 78 deductibility records, and Exempt Organization Business Master Files (EO-BMF) from NBER. The script handles longitudinal data standardization across multiple filing formats and regulatory changes over time (2012-2022). 

*Dependencies: readxl, readr, stringr, dplyr 
Data Sources: Combined EO-BMF data, IRS Statistics of Income, IRS Publication 78*

3: **Census Tract Data Collection Script (census_geography_downloader.py)**: Created automated web scraping and geospatial processing script that downloads all shapefiles from the Census Bureau's TIGER/Line database for 2000, 2010, and 2020 for Counties, Census Tracts, Census Block Groups, Congressional Districts, American Indian / Alaska Native / Native Hawaiian Areas 2020 (AIANNH), . The script scrapes file links, downloads state-specific zip archives, extracts shapefiles, and combines them into a single nationwide area-specific shapefiles for spatial analysis.
  
*Dependencies: geopandas, pandas, beautifulsoup4, requests*

4: **Multi-Temporal Census Geography Standardization Pipeline (census_geography_standardizer.py):** : This script standardizes and harmonizes U.S. Census TIGER/Line shapefiles across three decades (2000, 2010, 2020) for five geographic levels: Census Tracts, Counties, Block Groups, Native American Areas, and Congressional Districts. The pipeline transforms raw census shapefiles into analysis-ready datasets with consistent schemas and organized file structure.

*Dependencies: geopandas, pandas, os
Input: Raw Census TIGER/Line shapefiles from downloader script*


5: **Batch Geocoding and Export Script (batch_geocoder.py):** ArcPy-based geocoding workflow that processes multiple CSV files containing address data, converts them to geographic coordinates using ArcGIS locator services, and exports results in multiple formats. The script automatically processes state-year combinations, creates organized output directories, and generates both shapefile and delimited text outputs. 

*Dependencies: arcpy, pandas, numpy
Requirements: ArcGIS Desktop/Pro license, configured address locator*

6: **Spatial Join and Geographic Attribution Pipeline (nonprofit_spatial_attribution.py):** This script performs spatial joins between geocoded nonprofit organizations and multi-level Census geographic boundaries to assign geographic identifiers to each organization. The system processes nonprofit address data across multiple decades (2000s, 2010s, 2020s) by state-year combinations and attributes them with corresponding Census Tract, County, Block Group, Congressional District, and Native American Area identifiers based on their spatial location.

*Dependencies: geopandas, pandas, os, re, numpy
Input: Geocoded nonprofit shapefiles, standardized Census boundary files
Temporal Logic: Uses 2000 boundaries for 2000-2009 data, 2010 boundaries for 2010-2019 data, 2020 boundaries for 2020+ data*

7: **IRS Form 990 PDF Data Extraction Script (irs_990_pdf_scraper.py):** Comprehensive web scraping and OCR pipeline that downloads IRS Form 990 PDF archives by year, extracts specific pages, converts them to images, and uses optical character recognition to parse government grant data. The script processes 1M+ nonprofit tax filings to create structured datasets of organizational financial information.

*Dependencies: beautifulsoup4, requests, pypdf, pytesseract, pdf2image, PIL, pandas
Requirements: Tesseract OCR installation, substantial storage space for PDF processing*
