import geopandas 
import pandas
from bs4 import BeautifulSoup
import requests
import os
import re
import urllib.request
import zipfile

#2020 CENSUS TRACT DOWNLOADING BEGINS
#Using Beautiful Soup to extract 2020 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2020/TRACT/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for census tracts, by state from the Census website:
links = []
def tl(href):
    return href and re.compile("tl_2020_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)

#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)

#Importing the zip files from the Census website
for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)

#Make a new directory for the downloaded zip files:
newpath20= "your_directory/Census_Tracts_20"
os.mkdir(newpath20)

#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join('your_directory', link)
    d_folders.append(t)

#After downloading Census Tract 2010 data, unzip the files and delete the zipped files
for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath20)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Now making a list of the unique shapefiles in the Census Tracts 2020 folder:
shapefiles = []

for file in os.listdir(newpath20):
    if file.endswith(".shp"):
        wo = os.path.join(newpath20, file)
        shapefiles.append(wo)

#Take those Census tract 2020 shapefiles and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
census_tracts20 = os.path.join(newpath20, "census_tracts20.shp")
gdf.to_file(census_tracts20)
print("done")
#2020 CENSUS TRACT DATA PREPARATION ENDS

#2010 CENSUS TRACT DOWNLOADING BEGINS
#Using Beautiful Soup to extract 2010 Census website info:

html = 'https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2010/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for census tracts, by state from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_[0-9]{2}_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)

#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath10= "your_directory/Census_Tracts_10"
os.mkdir(newpath10)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census Tract 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath10)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Now making a list of the unique shapefiles in the Census Tracts 2010 folder:
shapefiles = []

for file in os.listdir(newpath10):
    if file.endswith(".shp"):
        wo = os.path.join(newpath10, file)
        shapefiles.append(wo)

#Take those Census tract 2010 shapefiles and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
census_tracts10 = os.path.join(newpath10, "census_tracts10.shp")
gdf.to_file(census_tracts10)
print("done")
#2010 CENSUS TRACT DATA PREPARATION ENDS

#2000 CENSUS TRACT DOWNLOADING BEGINS
#Using Beautiful Soup to extract 2000 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/TRACT/2000/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for census tracts, by state from the Census website:
links = []
import re
def tl(href):
    return href and re.compile("tl_2010_[0-9]{2}_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)

#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:

newpath00= "your_directory/Census_Tracts_00"
os.mkdir(newpath00)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    
#After downloading Census Tract 2000 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath00)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Now making a list of the unique shapefiles in the Census Tracts 2010 folder:
shapefiles = []

for file in os.listdir(newpath00):
    if file.endswith(".shp"):
        wo = os.path.join(newpath00, file)
        shapefiles.append(wo)

#Take those Census tract 2010 shapefiles and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
census_tracts00 = os.path.join(newpath00, "census_tracts00.shp")
gdf.to_file(census_tracts00)
print("done")
#2000 CENSUS TRACT DATA PREPARATION ENDS

#DOWNLOAD AND UNZIP ALL COUNTY FILES:
#COUNTY FILES FOR 2020
#Using Beautiful Soup to extract 2020 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2020/COUNTY/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for counties from the Census website:
links = []
import re
def tl(href):
    return href and re.compile("tl_2020_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website
import urllib.request
for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath20c= "your_directory/Counties_20"
os.mkdir(newpath20c)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census County 2020 data, unzip the files and delete the zipped files
import zipfile
for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath20c)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Finding the filename for the shape file
 
for file in os.listdir(newpath20c):
    if file.endswith(".shp"):
        counties_20 = os.path.join(newpath20c, file)
print("done")

#COUNTY FILES FOR 2010 
#Using Beautiful Soup to extract 2010 Census website info:
 
html = 'https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for counties from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath10c= "your_directory/Counties_10"
os.mkdir(newpath10c)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census County 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath10c)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Finding the filename for the shape file
 
for file in os.listdir(newpath10c):
    if file.endswith(".shp"):
        counties_10 = os.path.join(newpath10c, file)
print("done")

#COUNTY FILES FOR 2000
#Using Beautiful Soup to extract 2000 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2000/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for counties from the Census website:
links = []
import re
def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
 
newpath00c= "your_directory/Counties_00"
os.mkdir(newpath00c)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census County 2000 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath00c)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Finding the filename for the shape file
 
for file in os.listdir(newpath00c):
    if file.endswith(".shp"):
        counties_00 = os.path.join(newpath00c, file)
print("done")

#CENSUS BLOCK GROUP FILES FOR 2020
#Using Beautiful Soup to extract 2020 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2020/BG/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []
import re
def tl(href):
    return href and re.compile("tl_2020").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath20bg= "your_directory/BlockGroups_20"
os.mkdir(newpath20bg)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census Block Group 2020 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath20bg)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Now making a list of the unique shapefiles in the folder:
shapefiles = []
 
for file in os.listdir(newpath20bg):
    if file.endswith(".shp"):
        wo = os.path.join(newpath20bg, file)
        shapefiles.append(wo)

#Take those shapefiles in the folder and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
bgs_20 = os.path.join(newpath20bg, "bgs_20.shp")
gdf.to_file(bgs_20)
print("done")

#CENSUS BLOCK GROUP FILES FOR 2010
#Using Beautiful Soup to extract 2010 Census website info:

html = 'https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_[0-9]{2}_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath10bg= "your_directory/BlockGroups_10"
os.mkdir(newpath10bg)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census Block Group 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath10bg)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Now making a list of the unique shapefiles in the folder:
shapefiles = []
 
for file in os.listdir(newpath10bg):
    if file.endswith(".shp"):
        wo = os.path.join(newpath10bg, file)
        shapefiles.append(wo)

#Take those shapefiles in the folder and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
bgs_10 = os.path.join(newpath10bg, "bgs_10.shp")
gdf.to_file(bgs_10)
print("done")

#CENSUS BLOCK GROUP FILES FOR 2000
#Using Beautiful Soup to extract 2000 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/BG/2000/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files for counties from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_[0-9]{2}_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
 
newpath00bg= "your_directory/BlockGroups_00"
os.mkdir(newpath00bg)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading Census Block Group 2000 data, unzip the files and delete the zipped files
import zipfile
for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath00bg)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Now making a list of the unique shapefiles in the folder:
shapefiles = []
 
for file in os.listdir(newpath00bg):
    if file.endswith(".shp"):
        wo = os.path.join(newpath00bg, file)
        shapefiles.append(wo)

#Take those shapefiles in the folder and combine them into one shapefile
len(shapefiles)
gdflist=[]
for file in shapefiles:
    f = geopandas.read_file(file)
    gdflist.append(f)
gdf = pandas.concat(gdflist)
#Exporting that shapefile
bgs00 = os.path.join(newpath00bg, "bgs00.shp")
gdf.to_file(bgs00)

#American Indian / Alaska Native / Native Hawaiian Areas 2020 (AIANNH)
#Using Beautiful Soup to extract 2020 Census website info:

html = 'https://www2.census.gov/geo/tiger/TIGER2020/AIANNH/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2020_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath20nat= "your_directory/nativeareas_20"
os.mkdir(newpath20nat)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2020 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath20nat)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Identify the name of the shape file in the folder:
 
for file in os.listdir(newpath20nat):
    if file.endswith(".shp"):
        nativeareas_20 = os.path.join(newpath20nat, file)
print("done")

#American Indian / Alaska Native / Native Hawaiian Areas 2010 (AIANNH)
#Using Beautiful Soup to extract 2010 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/AIANNH/2010/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath10nat= "your_directory/nativeareas_10"
os.mkdir(newpath10nat)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath10nat)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
#Identify the name of the shape file in the folder:
 
for file in os.listdir(newpath10nat):
    if file.endswith(".shp"):
        nativeareas_10 = os.path.join(newpath10nat, file)
print("done")

#American Indian / Alaska Native / Native Hawaiian Areas 2000 (AIANNH)
#Using Beautiful Soup to extract 2000 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/AIANNH/2000/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
 
newpath00nat= "your_directory/nativeareas_00"
os.mkdir(newpath00nat)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2000 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath00nat)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Identify the name of the shape file in the folder:
 
for file in os.listdir(newpath00nat):
    if file.endswith(".shp"):
        nativeareas_00 = os.path.join(newpath00nat, file)
print("done")

#Congressional Districts 2020
#Using Beautiful Soup to extract 2020 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2020/CD/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2020_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath20cd= "your_directory/cd_20"
os.mkdir(newpath20cd)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2020 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath20cd)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Identify the name of the shape file in the folder:
 
for file in os.listdir(newpath20cd):
    if file.endswith(".shp"):
        cd_20 = os.path.join(newpath20cd, file)
print("done")

#Congressional Districts 2010
#Using Beautiful Soup to extract 2010 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/CD/111/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath10cd= "your_directory/cd_10"
os.mkdir(newpath10cd)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath10cd)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Identify the name of the shape file in the folder:
 
for file in os.listdir(newpath10cd):
    if file.endswith(".shp"):
        cd_10 = os.path.join(newpath10cd, file)
print("done")

#Congressional Districts 2000

#Using Beautiful Soup to extract 2000 Census website info:
html = 'https://www2.census.gov/geo/tiger/TIGER2010/CD/108/'
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')
#Extract the names of zip files from the Census website:
links = []

def tl(href):
    return href and re.compile("tl_2010_us_").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    links.append(a)
#Save those individual zip files as htmls in preparation for retrieval:
htmls = []
for l in links:
    h = html+l
    htmls.append(h)
    #Importing the zip files from the Census website

for idx, html in enumerate(htmls):
    filename = links[idx]
    filepath = os.path.join('your_directory', filename)
    urllib.request.urlretrieve(html, filepath)
    #Make a new directory for the downloaded zip files:
newpath00cd= "your_directory/cd_00"
os.mkdir(newpath00cd)
#Save the names of the downloaded file paths:
d_folders= []
for link in links:
    t = os.path.join(r'your_directory', link)
    d_folders.append(t)
    #After downloading 2010 data, unzip the files and delete the zipped files

for d_folder in d_folders:
    with zipfile.ZipFile(d_folder, 'r') as zip_ref:
        zip_ref.extractall(newpath00cd)
    #Then remove the zipped files themselves from the download directory:   
    os.remove(d_folder)
    #Identify the name of the shape file in the folder:

for file in os.listdir(newpath00cd):
    if file.endswith(".shp"):
        cd_00 = os.path.join(newpath00cd, file)
print("done")
