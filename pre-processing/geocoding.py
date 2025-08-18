import pandas as pd
import numpy as np
import arcpy, os
from arcpy import env
from arcpy.sa import *

#put your csvs in this directory:
csv_dir = r"C:/your_location_here"
os.chdir(csv_dir)

workspace = os.getcwd()
file_names = os.listdir(workspace)

#put your locator in this directory:
locator = r"C:\your_location_here"

#put your results in this directory:
results_dir = r"C:\your_location_here"

field_map = "Address street VISIBLE NONE; City city VISIBLE NONE; Region state VISIBLE NONE; Postal zip VISIBLE NONE"

for file in file_names:
    table = pd.read_csv(file)
    state = '[A-Z]+'
    state = re.findall(state, file)
    state =''.join(state)
    year = '^[0-9]+'
    year = re.findall(year, file)
    year = ''.join(year)
    combined = year+state 
    geocode_result = os.path.join(results_dir, combined) 
    os.mkdir(geocode_result)
    geocode_result2 = os.path.join(results_dir, combined, combined)
    merged_file = year+state+'merged_v2.csv'
    csv = os.path.join(csv_dir, merged_file)
    arcpy.GeocodeAddresses_geocoding(csv, locator, field_map, geocode_result2) 
    input_file = geocode_result2 + '.shp'
    fields = arcpy.ListFields(input_file)
    field_text = list()
    for f in fields:
        if f.type != "Geometry":
            field_text.append(f.name)
    output_file = geocode_result2+'.txt'
    arcpy.stats.ExportXYv(input_file, field_text, "SEMI-COLON", output_file, "ADD_FIELD_NAMES")
    print(state+year+" done!")
print("Geocoding complete")

