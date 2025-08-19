#Getting the directories for all the Census datasets in one place: 
#Census Tracts
import os
newpath20= "your_directory/Census_Tracts_20"
newpath10= "your_directory/Census_Tracts_10"
newpath00= "your_directory/Census_Tracts_00"

census_tracts_20 = os.path.join(newpath20, "census_tracts20.shp")
census_tracts_10 = os.path.join(newpath10, "census_tracts10.shp")
census_tracts_00 = os.path.join(newpath00, "census_tracts00.shp") 

#Counties
newpath20c= "your_directory/Counties_20"
newpath10c= "your_directory/Counties_10"
newpath00c= "your_directory/Counties_00"

file = "tl_2020_us_county.shp"
counties_20 = os.path.join(newpath20c, file)
file = "tl_2010_us_county10.shp"
counties_10 = os.path.join(newpath10c, file)
file = "tl_2010_us_county00.shp" 
counties_00 = os.path.join(newpath00c, file)

#Block Groups
newpath20bg= "your_directory/BlockGroups_20"
newpath10bg= "your_directory/BlockGroups_10"
newpath00bg= "your_directory/BlockGroups_00"

bgs_20 = os.path.join(newpath20bg, "bgs20.shp")
bgs_10 = os.path.join(newpath10bg, "bgs10.shp") 
bgs_00 = os.path.join(newpath00bg, "bgs00.shp") 

#American Indian / Alaska Native / Native Hawaiian Areas
newpath20nat= "your_directory/nativeareas_20"
newpath10nat= "your_directory/nativeareas_10"
newpath00nat= "your_directory/nativeareas_00"

file= "tl_2020_us_aiannh.shp"
nativeareas_20 = os.path.join(newpath20nat, file)
file= "tl_2010_us_aiannh10.shp"
nativeareas_10 = os.path.join(newpath10nat, file)
file= "tl_2010_us_aiannh00.shp"
nativeareas_00 = os.path.join(newpath00nat, file) 

#Congressional Districts
newpath20cd= "your_directory/cd_20"
newpath10cd= "your_directory/cd_10"
newpath00cd= "your_directory/cd_00"

file = "tl_2020_us_cd116.shp"
cd_20 = os.path.join(newpath20cd, file)
file = "tl_2010_us_cd111.shp"
cd_10 = os.path.join(newpath10cd, file) 
file = "tl_2010_us_cd108.shp" 
cd_00 = os.path.join(newpath00cd, file)

print("done")

import geopandas
#Reading in all Relevant TIGER shape files:

#Census Tracts
tracts00 = geopandas.read_file(census_tracts_00)
tracts10 = geopandas.read_file(census_tracts_10)
tracts20 = geopandas.read_file(census_tracts_20)

#Do I need to change column names in the 2000 data to match the 2010 and 2020 census??
#Change column names in 2010 Census data to match 2020 Census data column names: (remove the 10 from the column names)
tracts10.columns = tracts10.columns.str.rstrip('10')
tracts00.columns=tracts00.columns.str.rstrip('00')

#############
#ONLY RUN THE FOLLOWING LINES FOR THE CENSUS_TIDY DATASET, WHICH WAS CREATED FOR THE MERGE WITH 8872A and 8872B FILES ONLY.
tracts00 = tracts00.rename(columns={'CTIDFP': 'GEOID'})

#Reduce the number of columns to keep only the essential ones for the merge:
usecols= ['GEOID', 'geometry']
tracts00 = tracts00[usecols]
tracts10 = tracts10[usecols]
tracts20 = tracts20[usecols]
##################

#Add dataset name to beginning of all column names:
tracts00 = tracts00.add_prefix('TR')
tracts10 = tracts10.add_prefix('TR')
tracts20 = tracts20.add_prefix('TR')

#Remove that prefix from the geometry column only:
tracts00 = tracts00.rename(columns={'TRgeometry': 'geometry'})
tracts10 = tracts10.rename(columns={'TRgeometry': 'geometry'})
tracts20 = tracts20.rename(columns={'TRgeometry': 'geometry'})
print("done")

#Counties
counties00 = geopandas.read_file(counties_00)
counties10 = geopandas.read_file(counties_10)
counties20 = geopandas.read_file(counties_20) 

#Change column names in 2010 Census data to match 2020 Census data column names: (remove the 10 from the column names)
counties10.columns = counties10.columns.str.rstrip('10')
counties00.columns = counties00.columns.str.rstrip('00')

#############
#ONLY RUN THE FOLLOWING LINES FOR THE CENSUS_TIDY DATASET, WHICH WAS CREATED FOR THE MERGE WITH 8872A and 8872B FILES ONLY.
#RENAME 2000 counties geoID column to match the other datasets:
counties00 = counties00.rename(columns={'CNTYIDFP': 'GEOID'})

#Reduce the number of columns to keep only the essential ones for the merge:
usecols= ['STATEFP', 'GEOID', 'NAME', 'NAMELSAD', 'geometry']
counties00 = counties00[usecols]
counties10 = counties10[usecols]
counties20 = counties20[usecols]

#############

#Add dataset name to beginning of all column names:
counties00 = counties00.add_prefix('CO')
counties10 = counties10.add_prefix('CO')
counties20 = counties20.add_prefix('CO')
#Remove that prefix from the geometry column only:
counties00 = counties00.rename(columns={'COgeometry': 'geometry'})
counties10 = counties10.rename(columns={'COgeometry': 'geometry'})
counties20 = counties20.rename(columns={'COgeometry': 'geometry'})
print("done")

#Block Groups
bgs00 = geopandas.read_file(bgs_00)
bgs10 = geopandas.read_file(bgs_10)
bgs20 = geopandas.read_file(bgs_20)

#Change column names in 2010 Census data to match 2020 Census data column names: (remove the 10 from the column names)
bgs10.columns = bgs10.columns.str.rstrip('10')
bgs00.columns = bgs00.columns.str.rstrip('00')

#############
#ONLY RUN THE FOLLOWING LINES FOR THE CENSUS_TIDY DATASET, WHICH WAS CREATED FOR THE MERGE WITH 8872A and 8872B FILES ONLY.

bgs00 = bgs00.rename(columns={'BKGPIDFP': 'GEOID'})

#Reduce the number of columns to keep only the essential ones for the merge:
usecols= ['GEOID', 'geometry']
bgs00 = bgs00[usecols]
bgs10 = bgs10[usecols]
bgs20 = bgs20[usecols]
#############

#Add dataset name to beginning of all column names:
bgs00 = bgs00.add_prefix('BG')
bgs10 = bgs10.add_prefix('BG')
bgs20 = bgs20.add_prefix('BG')
#Remove that prefix from the geometry column only:
bgs00 = bgs00.rename(columns={'BGgeometry': 'geometry'})
bgs10 = bgs10.rename(columns={'BGgeometry': 'geometry'})
bgs20 = bgs20.rename(columns={'BGgeometry': 'geometry'})
print("done")

#American Indian / Alaska Native / Native Hawaiian Areas (AIANNH)
nativeareas00 = geopandas.read_file(nativeareas_00)
nativeareas10 = geopandas.read_file(nativeareas_10)
nativeareas20 = geopandas.read_file(nativeareas_20)

#Change column names in 2010 Census data to match 2020 Census data column names: (remove the 10 from the column names)
nativeareas10.columns = nativeareas10.columns.str.rstrip('10')
nativeareas00.columns = nativeareas00.columns.str.rstrip('00')

#############
#ONLY RUN THE FOLLOWING LINES FOR THE CENSUS_TIDY DATASET, WHICH WAS CREATED FOR THE MERGE WITH 8872A and 8872B FILES ONLY.

nativeareas00 = nativeareas00.rename(columns={'AIANNHID': 'GEOID'})

#Reduce the number of columns to keep only the essential ones for the merge:
usecols= ['GEOID', 'NAMELSAD', 'geometry']
nativeareas00 = nativeareas00[usecols]
nativeareas10 = nativeareas10[usecols]
nativeareas20 = nativeareas20[usecols]
#############

#Add NT to the beginning of all column names
nativeareas00 = nativeareas00.add_prefix('NT')
nativeareas10 = nativeareas10.add_prefix('NT')
nativeareas20 = nativeareas20.add_prefix('NT')

#Remove that prefix from the geometry column only:
nativeareas00 = nativeareas00.rename(columns={'NTgeometry': 'geometry'})
nativeareas10 = nativeareas10.rename(columns={'NTgeometry': 'geometry'})
nativeareas20 = nativeareas20.rename(columns={'NTgeometry': 'geometry'})
print("done")

#Saving the names of columns in the Census Native Areas dataset:
nativecol= []
for col in nativeareas10.columns:
    nativecol.append(col)

#Congressional Districts
cd00 = geopandas.read_file(cd_00)
cd10 = geopandas.read_file(cd_10)
cd20 = geopandas.read_file(cd_20)

#Change column names in 2010 Census data to match 2020 Census data column names: (remove the 10 from the column names)
cd10.columns = cd10.columns.str.rstrip('10')
cd00.columns = cd00.columns.str.rstrip('00')

cd00= cd00.rename(columns={"CD108FP": "FP"})
cd10= cd10.rename(columns={"CD111FP": "FP"})
cd20= cd20.rename(columns={"CD116FP": "FP"})

#Drop the STATENS variable from the 2010 data, as the 2020 data does not contain it:
cd10 = cd10.drop('STATENS', axis=1)

#############
#ONLY RUN THE FOLLOWING LINES FOR THE CENSUS_TIDY DATASET, WHICH WAS CREATED FOR THE MERGE WITH 8872A and 8872B FILES ONLY.

#Reduce the number of columns to keep only the essential ones for the merge:
usecols= ['FP', 'geometry']
cd00 = cd00[usecols]
cd10 = cd10[usecols]
cd20 = cd20[usecols]
#############

#Add CD to the beginning of all column names
cd00 = cd00.add_prefix('CD')
cd10 = cd10.add_prefix('CD')
cd20 = cd20.add_prefix('CD')
#Remove that prefix from the geometry column only:
cd00 = cd00.rename(columns={'CDgeometry': 'geometry'})
cd10 = cd10.rename(columns={'CDgeometry': 'geometry'})
cd20 = cd20.rename(columns={'CDgeometry': 'geometry'})
print("done")

#Create new folders under a larger umbrella folder entitled "Census_Tidy"
census_tidy = 'your_directory/Census_Tidy'
os.mkdir(census_tidy)
census_files = ["nativeareas_00", "nativeareas_10", "nativeareas_20", 'cd_00', 'cd_10', 'cd_20', 'BlockGroups_00', 'BlockGroups_10', 'BlockGroups_20', 'Counties_00', 'Counties_10', 'Counties_20', 'CensusTracts_00', 'CensusTracts_10', 'CensusTracts_20']
for i in census_files:
    os.mkdir(os.path.join(census_tidy, i))
print('done')

#Save the files as shp files:
nativeareas00.to_file(os.path.join(census_tidy, census_files[0], census_files[0]+'_tidy.shp'))
nativeareas10.to_file(os.path.join(census_tidy, census_files[1], census_files[1]+'_tidy.shp'))
nativeareas20.to_file(os.path.join(census_tidy, census_files[2], census_files[2]+'_tidy.shp'))

cd00.to_file(os.path.join(census_tidy, census_files[3], census_files[3]+'_tidy.shp'))
cd10.to_file(os.path.join(census_tidy, census_files[4], census_files[4]+'_tidy.shp'))
cd20.to_file(os.path.join(census_tidy, census_files[5], census_files[5]+'_tidy.shp'))

bgs00.to_file(os.path.join(census_tidy, census_files[6], census_files[6]+'_tidy.shp'))
bgs10.to_file(os.path.join(census_tidy, census_files[7], census_files[7]+'_tidy.shp'))
bgs20.to_file(os.path.join(census_tidy, census_files[8], census_files[8]+'_tidy.shp'))

counties00.to_file(os.path.join(census_tidy, census_files[9], census_files[9]+'_tidy.shp'))
counties10.to_file(os.path.join(census_tidy, census_files[10], census_files[10]+'_tidy.shp'))
counties20.to_file(os.path.join(census_tidy, census_files[11], census_files[11]+'_tidy.shp'))

tracts00.to_file(os.path.join(census_tidy, census_files[12], census_files[12]+'_tidy.shp'))
tracts10.to_file(os.path.join(census_tidy, census_files[13], census_files[13]+'_tidy.shp'))
tracts20.to_file(os.path.join(census_tidy, census_files[14], census_files[14]+'_tidy.shp'))
print("done")
