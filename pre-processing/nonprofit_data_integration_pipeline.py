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
mini_dir = "your_directory" + '/Mini_Joined'
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

#Extract the tax year and tract geoids from this file:
tractinfo= ngos[['tax_year','TRGEOID']]
print('tract info created')
del(ngos)
tractinfo.to_csv('your_directory/tractinfo.csv')
print('done')

#Create new folder to contain data with geospatial joined features *and* full IRS financial data (not just EOBMF data):
#This is only going to be possible for 2012 and after because those are the only years I have full IRS financial data for:
#os.mkdir("your_directory/Geojoined_990")

geojoined_dir = "your_directory/Geojoined_990"
os.mkdir(geojoined_dir)

all_files = os.listdir(mini_dir)
after2012 = []

phrase1 = '201[2-9]{1}.*'
phrase2 = '20[2-9]{1}[0-9]{1}.*'

import re 
import os
for file in all_files:
    a = re.findall(phrase1, str(file))
    if(len(a)==0):
        a = re.findall(phrase2, str(file))
        if(len(a)>0):
            after2012.append(a[0])
    else:
        after2012.append(a[0])

#Create new subfolders for each year, state, type of filing (eg. "2010CAEZ", "2019ND990")
for folder in after2012:
    ez = folder+ "EZ"
    reg = folder+ "990"
    path = os.path.join(geojoined_dir, ez)
    os.mkdir(path)
    path = os.path.join(geojoined_dir, reg)
    os.mkdir(path)
    print(path, ' created!')

#Loading in the IRS EZ files:
downloads = "your_directory"
ezfile = "ez_1220_efficient.csv"
ezfile = os.path.join(downloads, ezfile)
ez = pandas.read_csv(ezfile)

#Loading in the IRS 990 files:
regfile = "full_reg_efficient.csv"
regfile = os.path.join(downloads, regfile)
reg = pandas.read_csv(regfile)
print("done")

#***STEP 2
#All of the EINs in these two datasets end in '.0'. In addition, some of the EINs are less than 9 characters long, and thus 
#need '0's appended to the front.

#Eliminate '.0' from the end of the EINS in both the 990(reg) and ez datasets
datasets = [ez, reg]

for dat in datasets:
    #Create a tax year column for both datasets
    s= dat['tax_pd'].astype(str)
    dat['tax_year'] = s.str.extract(r'(\d{4})')
    dat['tax_year'] =dat['tax_year'].astype(str)
    dat['ein']= dat['ein'].astype(str)
    
    #Making sure that the EINs all have a length of 9 characters, starting with zeros if they are 8 or 7 characters long
    eins = dat['ein'].tolist()
    phrase = r"[0-9]+(?=\.)"

    new_eins = []
    for ein in eins:
        num = re.findall(phrase, ein)
        num =''.join(num)
        new_eins.append(num)
    
    c = []
    for ein in new_eins:
        if(len(ein)==8):
            c.append('0'+ein)
        elif(len(ein)==7):
            c.append('00'+ein)
        else:
            c.append(ein)
        
    new_eins=c
    #Take this new list of EINs and replace the existing list of EINs in the dataset:
    dat['ein'] = new_eins
    print(dat, "done")

#Merging geo-coded 990 EO-BMF data with full 990 and 990EZ filings for each EIN-year entry in my dataset:

for folder in after2012:
    filename = folder + "minijoined.csv" 
    fileloc = os.path.join(mini_dir, folder, filename)
    df = pandas.read_csv(fileloc, low_memory=False)

    #DON'T THINK I NEED THIS ENTIRE SECTION
    #Making sure that the tax years are integer values and EINs are string values:
    df['ein'] = df['ein'].astype(str) #make this a character value
    df['tax_year'] = df['tax_year'].astype(str) #make this a character value

    #DON'T THINK I NEED THIS ENTIRE SECTION EITHER
    #Make sure that all EINs have the same number of characters (some have 7 or 8, and those should start with a zero):
    c = []
    for ein in df['ein']:
        if(len(ein)==8):
            c.append('0'+ein)
        elif(len(ein)==7):
            c.append('00'+ein)
        else:
            c.append(ein)
    df['ein'] = c

    #Merge the Joined CSV file with the 2012-2020 990 Return dataframe:
    merged_ez = pandas.merge(df, ez, how='inner', on=['ein', 'tax_year'])
    merged_reg = pandas.merge(df, reg, how='inner', on=['ein', 'tax_year'])

    newname_ez = os.path.join(geojoined_dir, folder+'EZ', "EZgeojoined.csv")
    newname_reg = os.path.join(geojoined_dir, folder+'990', "990geojoined.csv")
    
    #Save the geojoined file to the new working directory as csv file:
    merged_ez.to_csv(newname_ez, sep=',', index=False, header=True)
    merged_reg.to_csv(newname_reg, sep=',', index=False, header=True)
    print(folder, "complete")
    
    #Clear space in memory for the next round
    del(merged_reg)
    del(merged_ez)

#Combine all of the full 990s together into one dataframe:

geojoined_dir = 'your_directory/GeoJoined_990'
phrase = r'[0-9]{4}[A-Z]{2}990'
year = r'[0-9]{4}'
geojoined_990 = []
years = [*range(2012,2021, 1)] #Creating a list of years that my ACS variables will cover

for folder in os.listdir(geojoined_dir): 
    if re.match(phrase, folder):
        geojoined_990.append(folder)


for y in years:
    counter =1
    for f in geojoined_990:
        if(re.findall(year, f)[0]==str(y)):
            if counter==1:
                ngos = pd.read_csv(os.path.join(geojoined_dir, f, '990geojoined.csv'))
            else:
                ngos2 = pd.read_csv(os.path.join(geojoined_dir, f, '990geojoined.csv'))
                ngos = pd.concat([ngos, ngos2])
                print(f, ' done!')
            counter = counter +1
    else:
        print('next!')
    ngos.to_csv('your_directory/GeoJoined_990/full_990_'+str(y)+'.csv')

#Combine all EZs together into one dataframe:

geojoined_dir = 'your_directory/GeoJoined_990'
phrase = r'[0-9]{4}[A-Z]{2}EZ'
year = r'[0-9]{4}'
geojoined_990 = []
years = [*range(2012,2021, 1)] #Creating a list of years that my ACS variables will cover

for folder in os.listdir(geojoined_dir): 
    if re.match(phrase, folder):
        geojoined_990.append(folder)


for y in years:
    counter =1
    for f in geojoined_990:
        if(re.findall(year, f)[0]==str(y)):
            if counter==1:
                ngos = pd.read_csv(os.path.join(geojoined_dir, f, 'EZgeojoined.csv'))
            else:
                ngos2 = pd.read_csv(os.path.join(geojoined_dir, f, 'EZgeojoined.csv'))
                ngos = pd.concat([ngos, ngos2])
                print(f, ' done!')
            counter = counter +1
    else:
        print('next!')
    ngos.to_csv('your_directory/GeoJoined_990/EZ_'+str(y)+'.csv')

