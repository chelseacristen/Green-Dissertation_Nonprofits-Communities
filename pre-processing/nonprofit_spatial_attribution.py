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
    del(ngos)
    del(ntjoin)
print("spatial join complete")
