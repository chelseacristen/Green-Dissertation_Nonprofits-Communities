#Write each newly trimmed Census files to their own csvs in their own new folders
jointxt = pandas.DataFrame(join)
    
#Change working directory to joined folder name:
os.chdir(jpath)
    
#Save the spatially joined file to the new working directory as shp file:
join.to_file(joined_file_shp)
    
#Save the spatially joined file to the new working directory as csv file:
jointxt.to_csv(joined_file_txt, sep=',', index=False, header=True)
    
#Create a new working directory for spatially joined folder:
joined_dir = "your_directory" + '/Joined' 
os.mkdir(joined_dir)
print("done")
done
#Subset the number of files in my working directory to those with the years 2010 and beyond ONLY:
#IF the first four numbers in the folder name are greater than 2010, save those folder names into a new list:
import os
os.chdir(r"your_directory/Geocoded_Results")
workspace = os.getcwd()
folder_names = os.listdir(workspace)

import re     
phrase = r"20[1-9]{1}[0-9]{1}[A-Z]{2}"
after2010 = []
for folder in folder_names:
    if(re.match(phrase, folder)):
        after2010.append(folder)
print("done")

#Make sure the Native American column names are ready to go for later merge:
addcols = nativecol[:-1]
addcols= ["USER_ein"] + addcols
addcols_min1 = addcols[1:]
print("done")
done
done
#For every folder in this new list:
for folder in after2010:
    #Change directory to respective geocoded folder name:
    folder_path = os.path.join(workspace, folder)
    os.chdir(folder_path)
    
    #Create the name of my joined file for later:
    import re
    import numpy as np
    state = '[A-Z]+'
    state = re.findall(state, folder) 
    state =''.join(state)
    year = '^[0-9]+'
    year = re.findall(year, folder)
    year = ''.join(year)
    combined = year+state 
    shape_file = 'joined.shp'
    text_file = 'joined.csv'
    joined_file_shp = year + state + shape_file
    joined_file_txt = year + state + text_file
    
    #Create a new folder in the "Joined" directory for this state/year
    jpath = os.path.join(joined_dir, combined)
    os.mkdir(jpath)
    
    # Read the NGO address data in
    geocoded_shapefile = year + state +'.shp' 
    address_file = os.path.join(folder_path, geocoded_shapefile) 
    ngos = geopandas.read_file(address_file)
    
    #All of the NGO Address data was geocoded in WGS 1984 (4326). Because the revision date of the epsg 4269 is 2019, 
    #past most recent major 2011 change, and we are working in North America,
    #let's project all the address data to epsg:4269 too. (currently it's in WSG 1984, and I want to align the crs with the 
    #one that the Census uses for its shapefiles)
    ngos = ngos.to_crs(4269)
    year = int(year)
    
      #For files between 2010 and 2019:
    if ((year>=2010) and (year<= 2019)):
        join = geopandas.sjoin(ngos, counties10, how="inner", predicate="within") #counties spatial join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, tracts10, how="inner", predicate="within") #census tracts join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, bgs10, how="inner", predicate="within") #census block groups join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, cd10, how="inner", predicate="within") #congressional districts join
        join = join.drop(['index_right'], axis=1) #Delete index column
        ntjoin = geopandas.sjoin(ngos, nativeareas10, how="inner", predicate="within") #Native areas join
        ntjoin = ntjoin.drop(['index_right'], axis=1) #Delete index column
        #If there are NGOs located in Native Areas, merge the dataset with Native Area info
        if(len(ntjoin)>0):
            ntjoin = ntjoin[addcols]
            join = join.merge(ntjoin, on="USER_ein", how="left") 
        #Otherwise, create Native Area columns for the spatially joined dataset filled with NaN
        else:
            for col in addcols_min1:
                join[col] = np.nan
    
    #For files between 2020 and 2029:
    else:
        join = geopandas.sjoin(ngos, counties20, how="inner", predicate="within") #counties spatial join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, tracts20, how="inner", predicate="within") #census tracts join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, bgs20, how="inner", predicate="within") #census block groups join
        join = join.drop(['index_right'], axis=1) #Delete index column
        join = geopandas.sjoin(join, cd20, how="inner", predicate="within") #congressional districts join
        join = join.drop(['index_right'], axis=1) #Delete index column
        ntjoin = geopandas.sjoin(ngos, nativeareas20, how="inner", predicate="within") #Native areas join
        ntjoin = ntjoin.drop(['index_right'], axis=1) #Delete index column
         #If there are NGOs located in Native Areas, merge the dataset with Native Area info
        if(len(ntjoin)>0):
            ntjoin = ntjoin[addcols]
            join = join.merge(ntjoin, on="USER_ein", how="left") 
        #Otherwise, create Native Area columns for the spatially joined dataset filled with NaN
        else:
            for col in addcols_min1:
                join[col] = np.nan
    
    #Make the joined file a text file 
    jointxt = pandas.DataFrame(join)
    
    #Change working directory to joined folder name:
    os.chdir(jpath)
    
    #Save the spatially joined file to the new working directory as shp file:
    join.to_file(joined_file_shp)
    
    #Save the spatially joined file to the new working directory as csv file:
    jointxt.to_csv(joined_file_txt, sep=',', index=False, header=True)
    print(state, year, "complete")
    del(join)

#####JOIN GEOCODED AND CENSUS CATEGORIZATIONS (This is basically a repeat of the loop preceding this block because I decided
#later to do this join for the 2000s organizations!)
geocoded_dir = "your_directory/Geocoded_Results"
joined_dir = "your_directory" + '/Joined' 
  
phrase = r"200[0-9]{1}[A-Z]{2}"
after2000 = []
for folder in os.listdir(geocoded_dir):
    if(re.match(phrase, folder)):
        after2000.append(folder)

#Create new subfolders in the Joined Directory with all of the appropriate years and dates:
for folder in after2000:
    newdirectory = os.path.join(joined_dir, folder)
    os.mkdir(newdirectory)
###FOR THE 2000s dataset only, load the appropriate census files exactly the way it was done for the 2010s and 2020s:
#Reading in all Relevant TIGER shape files:

#Census Tracts
tracts00 = geopandas.read_file(census_tracts_00)
tracts00.columns=tracts00.columns.str.rstrip('00')
tracts00 = tracts00.add_prefix('TR')
tracts00 = tracts00.rename(columns={'TRgeometry': 'geometry'})

counties00 = geopandas.read_file(counties_00)
counties00.columns = counties00.columns.str.rstrip('00')
counties00 = counties00.add_prefix('CO')
counties00 = counties00.rename(columns={'COgeometry': 'geometry'})

bgs00 = geopandas.read_file(bgs_00)
bgs00.columns = bgs00.columns.str.rstrip('00')
bgs00 = bgs00.add_prefix('BG')
bgs00 = bgs00.rename(columns={'BGgeometry': 'geometry'})

nativeareas00 = geopandas.read_file(nativeareas_00)
nativeareas00.columns = nativeareas00.columns.str.rstrip('00')
nativeareas00 = nativeareas00.add_prefix('NT')
nativeareas00 = nativeareas00.rename(columns={'NTgeometry': 'geometry'})


#Saving the names of columns in the Census Native Areas dataset:
nativecol= []
for col in nativeareas00.columns:
    nativecol.append(col)
    
#Make sure the Native American column names are ready to go for later merge:
addcols = nativecol[:-1]
addcols= ["USER_ein"] + addcols
addcols_min1 = addcols[1:]

cd00 = geopandas.read_file(cd_00)
cd00.columns = cd00.columns.str.rstrip('00')

cd00= cd00.rename(columns={"CD108FP": "FP"})
cd00 = cd00.add_prefix('CD')
cd00 = cd00.rename(columns={'CDgeometry': 'geometry'})

print("Census files loaded in")

for folder in after2000:
    #Change directory to respective geocoded folder name:
    folder_path = os.path.join(geocoded_dir, folder)
    os.chdir(folder_path)
    
    #Create the name of my joined file for later:
    state = '[A-Z]+'
    state = re.findall(state, folder) 
    state =''.join(state)
    year = '^[0-9]+'
    year = re.findall(year, folder)
    year = ''.join(year)
    combined = year+state 
    text_file = 'joined.csv'
    joined_file_txt = year + state + text_file
        
    # Read the NGO address data in
    geocoded_shapefile = year + state +'.shp' 
    address_file = os.path.join(folder_path, geocoded_shapefile) 
    ngos = geopandas.read_file(address_file)
    
    #All of the NGO Address data was geocoded in WGS 1984 (4326). Because the revision date of the epsg 4269 is 2019, 
    #past most recent major 2011 change, and we are working in North America,
    #let's project all the address data to epsg:4269 too. (currently it's in WSG 1984, and I want to align the crs with the 
    #one that the Census uses for its shapefiles)
    ngos = ngos.to_crs(4269)
    year = int(year)
    
    join = geopandas.sjoin(ngos, counties00, how="inner", predicate="within") #counties spatial join
    join = join.drop(['index_right'], axis=1) #Delete index column
    join = geopandas.sjoin(join, tracts00, how="inner", predicate="within") #census tracts join
    join = join.drop(['index_right'], axis=1) #Delete index column
    join = geopandas.sjoin(join, bgs00, how="inner", predicate="within") #census block groups join
    join = join.drop(['index_right'], axis=1) #Delete index column
    join = geopandas.sjoin(join, cd00, how="inner", predicate="within") #congressional districts join
    join = join.drop(['index_right'], axis=1) #Delete index column
    ntjoin = geopandas.sjoin(ngos, nativeareas00, how="inner", predicate="within") #Native areas join
    ntjoin = ntjoin.drop(['index_right'], axis=1) #Delete index column
        
    #If there are NGOs located in Native Areas, merge the dataset with Native Area info
    if(len(ntjoin)>0):
        ntjoin = ntjoin[addcols]
        join = join.merge(ntjoin, on="USER_ein", how="left") 
        #Otherwise, create Native Area columns for the spatially joined dataset filled with NaN
    else:
        for col in addcols_min1:
            join[col] = np.nan
    
    #Make the joined file a text file 
    jointxt = pandas.DataFrame(join)
    
    #Change working directory to joined folder name:
    os.chdir(os.path.join(joined_dir, combined))
    
    #Save the spatially joined file to the new working directory as csv file:
    jointxt.to_csv(joined_file_txt, sep=',', index=False, header=True)
    print(state, year, "complete")
    del(join)
    del(ngos)
    del(ntjoin)
print("spatial join complete")

del(nativeareas00)
del(cd00)
del(tracts00)
del(counties00)
del(bgs00)
del(ngos)
del(ntjoin)
print("spatial join complete")

#Create joined folder and subfolders, v2. This version cleans up EINs and clarifies fips codes for different Census areas:
joinedv2_dir = "your_directory" + '/Joinedv2' 
joined_dir = "your_directory" + '/Joined' 
os.mkdir(joinedv2_dir)

for idx, folder in enumerate(os.listdir(joined_dir)):
    #Create new joined subfolder in the version 2 folder:
    newdir = os.path.join(joinedv2_dir,folder)
    os.mkdir(newdir)
     
    #Save the name of the file containing NGO data I'm going to be working with in this iteration
    file = os.listdir(os.path.join(joined_dir, folder))[0]
    filepath = os.path.join(joined_dir, folder, file)
    
    #Create the name of my joined v2 file for later:
    new =folder+'joinedv2.csv'
    joinedv2_file = os.path.join(joinedv2_dir, folder, new)

    #Load the file in from its respective Joined folder and subfolder:
    ngos= pd.read_csv(filepath, low_memory=False)
    
    #1. Fix the EIN numbers so they are all 9 digits long. 
    #Making sure that the EINs all have a length of 9 characters, starting with zeros if they are 8 or 7 characters long
    ngos = ngos.astype({'USER_ein':'string'})
    c = []
    for ein in ngos['USER_ein']:
        if(len(ein)==8):
            c.append('0'+ein)
        elif(len(ein)==7):
            c.append('00'+ein)
        else:
            c.append(ein)
    ngos['USER_ein'] = c
    del(c)
    
    #Fixing the GEOIDs, making them just cleaner for future work.
    #1. State ID- rename 'COSTATEFP' to 'statefips'
    ngos = ngos.rename(columns={'COSTATEFP': 'STGEOID'})
    
    #Renaming fipscode columns for files merged specifically with 2000 census files to standardize them with 2010 and 2020 Census-based files
    phrase = r"200.*" 
    if(re.match(phrase, folder)):
        ngos = ngos.rename(columns={'COCNTYIDFP': 'COGEOID'})
        ngos = ngos.rename(columns={'TRCTIDFP': 'TRGEOID'})
        ngos = ngos.rename(columns={'BGBKGPIDFP': 'BGGEOID'})
        ngos = ngos.rename(columns={'NTAIANNHID': 'NTGEOID'})
        
    #For files from the 2000s, I actually have to create a congressional district geoid using pre-existing columns. 
    #First, formatting existing columns to do this properly:
        ngos = ngos.astype({'CDSTATEFP': 'string'})
        new = []
        for id in ngos['CDSTATEFP']:
            if(len(id)==1):
                new.append('0'+id)
            else: 
                new.append(id)   
        ngos['CDSTATEFP'] = new
    
        ngos = ngos.astype({'CDFP': 'string'})
        new = []
        for id in ngos['CDFP']:
            if(len(id)==1):
                new.append('0'+id)
            else: 
                new.append(id)   
        ngos['CDFP'] = new
    
        #Now finally creating the new CDGEOID column for files from 2000-2009:
        ngos["CDGEOID"] = ngos[["CDSTATEFP", "CDFP"]].apply("".join, axis=1)
    else:
        new = []
        ngos = ngos.astype({'CDGEOID': 'string'})
        for id in ngos['CDGEOID']:
            if(len(id)==3):
                new.append('0'+id)
            else: 
                new.append(id)   
        ngos['CDGEOID'] = new
    
    #Now making sure that all of my GEOID variables are string variables:
    ngos = ngos.astype({'COGEOID': 'string', 'TRGEOID': 'string', 'BGGEOID': 'string'})

    #fix countyfips so that if it is less than five digits, add a zero in front of it
    new = []
    for id in ngos['COGEOID']:
        if(len(id)==4):
            new.append('0'+id)
        else: 
            new.append(id)   
    ngos['COGEOID'] = new

    #fix tractfips so that if it is less than eleven digits, add a zero in front of it
    new = []
    for id in ngos['TRGEOID']:
        if(len(id)==10):
            new.append('0'+id)
        else: 
            new.append(id)   
    ngos['TRGEOID'] = new

    #fix bgfips so that if it is less than 12 digits, add a zero in front of it
    new = []
    for id in ngos['BGGEOID']:
        if(len(id)==11):
            new.append('0'+id)
        else: 
            new.append(id)   
    ngos['BGGEOID'] = new
    #Create new column: 'Nativearea': assign dummy variable 0/1 based on whether 'NTAIANNHCE' is NA or not. 
    c = []
    for id in ngos['NTAIANNHCE']:
        if(pd.isna(id)):
            c.append(0)
        else:
            c.append(1)
    ngos = ngos.assign(NATIVEAREA=c)
    
    #Drop cases where input error occured (RegionAbbr is not the same as IN_Region) from the ngos dataframe:
    index = ngos[(ngos['RegionAbbr'] != ngos['IN_Region']) ].index
    ngos.drop(index, inplace=True)
    
    #Export the ngos dataframe to new csv in the Joined Folder, v2
    ngos.to_csv(joinedv2_file)
   
    #Remove the dataframes to make space in memory for new ones
    del(ngos)

    print('done with ', folder)

joinedv2_dir = "your_directory" + '/Joinedv2' 

#Create new folder and subfolders to contain a MUCH scaled down version of the Joined folders and files. This will aid in data 
#analysis later, namely reducing the size of all the files.
mini_dir = "C:/Users/steve/Documents" + '/Mini_Joined'
os.mkdir(mini_dir)

for idx, folder in enumerate(os.listdir(joinedv2_dir)):
    
     #Create new joined subfolder in the mini version folder:
    newdir = os.path.join(mini_dir, folder)
    os.mkdir(newdir)
    
    #Save the name of the file containing NGO data I'm going to be working with in this iteration
    file = os.listdir(os.path.join(joinedv2_dir, folder))[0]
    filepath = os.path.join(joinedv2_dir, folder, file)
    
    #Create the name of my mini joined file for later:
    new=folder+'minijoined.csv'
    mini_file = os.path.join(mini_dir, folder, new)
    
    #Load the file in from its respective Joined folder and subfolder:
    ngos= pd.read_csv(filepath, low_memory=False)
   
    #Drop cases where input error occured (RegionAbbr is not the same as IN_Region) from the ngos dataframe:
    index = ngos[(ngos['RegionAbbr'] != ngos['IN_Region']) ].index
    ngos.drop(index, inplace=True)
    
    #Creating a smaller dataset for more manageable data analysis:
    #Subsetting to a limited number of columns:
    mini_ngos = ngos[['Score', 'Match_addr', 'Addr_type', 'X', 'Y', 'USER_ein', 'USER_name', 'USER_stree', 'USER_city', 'USER_state', 'USER_zip', 'USER_subse', 'USER_rulin', 'USER_rul_1', 'USER_found', 'USER_tax_y', 'USER_tax_m', 'USER_ntee1', 'USER_acct_', 'USER_filin', 'USER_pf_fi', 'USER_asset', 'USER_incom', 'USER_sort_', 'geometry', 'STGEOID', 'COGEOID', 'TRGEOID', 'BGGEOID', 'CDGEOID', 'NTGEOID']]

    #Rename columns in the mini_ngos file:
    mini_ngos = mini_ngos.rename(columns={'USER_ein': 'ein', 'USER_name': 'name', 'USER_stree': 'street', 'USER_city': 'city', 'USER_state': 'state', 'USER_zip': 'zip', 'USER_subse': 'subsection', 'USER_rulin': 'rule_y', 'USER_rul_1': 'rule_m', 'USER_found': 'foundation', 'USER_tax_y': 'tax_year', 'USER_tax_m': 'tax_month', 'USER_ntee1': 'ntee1', 'USER_acct_': 'acct_pd', 'USER_filin': 'filing', 'USER_pf_fi': 'pf_filing', 'USER_asset': 'assets', 'USER_incom': 'income', 'USER_sort_': 'sort_name'})
    
    #Create new column: 'Nativearea': assign dummy variable 0/1 based on whether 'NTAIANNHCE' is NA or not. 
    c = []
    for id in ngos['NTGEOID']:
        if(pd.isna(id)):
            c.append(0)
        else:
            c.append(1)
    ngos = ngos.assign(NATIVEAREA=c)
    
    #Save output to csv
    mini_ngos.to_csv(mini_file)
    
    #Remove the dataframes to make space in memory for new ones
    del(ngos)
    del(mini_ngos)

    print('done with ', folder)

#Create a combined file of all of these csvs for 2010 onward:
#Subset the number of files in my working directory to those with the years 2010 and beyond ONLY:
#IF the first four numbers in the folder name are greater than 2010, save those folder names into a new list:

mini_dir = "your_directory" + '/Mini_Joined'

phrase = r"20[1-9]{1}[0-9]{1}[A-Z]{2}"
counter=1

for folder in os.listdir(mini_dir):
    if(re.match(phrase, folder)):
        if counter== 1:
            ngos = pd.read_csv(os.path.join(mini_dir, folder, folder+'minijoined.csv'), low_memory=False)
            counter=2
        else:
            ngos2 = pd.read_csv(os.path.join(mini_dir, folder, folder+'minijoined.csv'), low_memory=False)
            ngos = pd.concat([ngos, ngos2])
        print(folder, "done")

#Export combined csv file:
ngos.to_csv(os.path.join(mini_dir, 'mini_combined.csv'))
print('final mini join exported')
