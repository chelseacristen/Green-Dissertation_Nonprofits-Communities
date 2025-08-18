#Using Beautiful Soup to identify and download zip files of IRS 990 PDFS
pages = [0, 8]
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import re
import zipfile
year='2021' #Insert the respective year here that you care about scraping from. I did this for 2016-2022.
html = 'https://www.irs.gov/charities-non-profits/form-990-series-downloads-'+year
html_page = requests.get(html)
soup = BeautifulSoup(html_page.content, 'html.parser')

#Extract the names of zip files for census tracts, by state from the Census website:
htmls = []
def tl(href):
    return href and re.compile(".zip").search(href)
files = soup.find_all(href=tl)
for link in files:
    a = link.get('href')
    htmls.append(a)

#Importing the zip files from the IRS website
zips = []
for idx, html in enumerate(htmls):
    zips.append(re.search('(?<=.pdf_).*(.zip)', html)[0])

#Fixing inconsistent formatting of HTMLs for downloading
htmls2 =[]
for html in htmls: 
    htmls2.append(re.search('.*(.zip)', html)[0])
htmls = htmls2
if year=='2017':
    htmls[85]= 'https://apps.irs.gov/pub/epostcard/990/2017/04/download990pdf_04_2017_prefixes_43-46.zip'

zips2 = []
for z in zips:
    zips2.append(re.sub('/','',z))
zips = zips2
print('done')



import urllib.request
from pypdf import PdfReader, PdfWriter
from PIL import Image
import pytesseract 
from pdf2image import convert_from_path
import numpy as np
import shutil
pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
directory = 'your_directory'

for idx, html in enumerate(htmls):
    #Create an empty dataframe with three columns:
    df= pd.DataFrame(columns=['ein', 'tax_year', 'gov_grants'])
    urllib.request.urlretrieve(html, os.path.join('your_directory', zips[idx]))
    newfolder = re.match('.*(?=.zip)', zips[idx])[0]
    os.mkdir(os.path.join('your_directory', newfolder)) #create new folder
    newfolder=os.path.join('your_directory', newfolder)

    with zipfile.ZipFile(os.path.join('your_directory', zips[idx]), 'r') as zip_ref: #Unzip folder:
        zip_ref.extractall(newfolder) #extract all files into new folder
    os.remove(os.path.join('your_directory', zips[idx]))
    
    for file in os.listdir(newfolder):
        string = re.findall('(?<=990).*', file)[0]
        if ((string[0]!='_') & (string[0]!='O')):
            os.remove(os.path.join(newfolder, file))
        elif ((file=='363904348_201512_990_2016123014045351.pdf')|
            (file=='221841274_201612_990_2017120615010925.pdf') |
                 (file=='731353370_201706_990_2018050715291363.pdf') | 
                 (file=='350905952_201706_990_2017122715052099.pdf')):
            os.remove(os.path.join(newfolder, file)) #this file is corrupted, so remove it.
        else:
            pdf_reader = PdfReader(os.path.join(newfolder, file))
            if len(pdf_reader.pages)<9:
                os.remove(os.path.join(newfolder, file))
            else:
                pdf_writer = PdfWriter()  # we want to reset this when starting a new pdf
                for i in pages:
                    pdf_writer.add_page(pdf_reader.pages[i])
                    output_filename = os.path.join(newfolder, file)
                with open(output_filename, "wb") as out:
                    pdf_writer.write(out)
    for f in os.listdir(newfolder):
        images = convert_from_path(os.path.join(newfolder,f))
        text = []
        for image in images:
            text.append(pytesseract.image_to_string(image, config='--psm 11'))
        text = ''.join(text)

    #Extract only the first observation as the EIN, as the second one is associated 
    #with the tax preparer
        if len(re.findall(r'\d{2}-[0-9]{7}', text))==0:
            ein = np.nan
        else:
            ein = re.findall(r'\d{2}-[0-9]{7}', text)[0] 

    #Extracting the tax year
        if len(re.findall(r'20\d{2}', text))==0:
            tax_year=np.nan
        else:
            tax_year = re.findall(r'20\d{2}', text)[0]

    #Extracting government grants 
        text = re.sub("\n", " ", text)
        if ' le ' in text:
            if re.search(' le (.*)All other con', text)==None:
                gov_grants= np.nan
            else:
                match = re.search(r' le (.*)All other con', text).group(1)
                if bool(re.search(r'\d\d\d+', match))==True:
                    matches = re.split(r'\s', match)
                    test = [x for x in matches if re.match(r'.*\d(\,|\d).*',x)][0]
                    gov_grants = int(re.sub(r'[^0-9]', "", test))
                else:
                    gov_grants = 0
        elif 'Government grants' in text:
            if re.search('Government grants(.*)All other con', text)==None:
                gov_grants= np.nan
            else:
                match= re.search('Government grants(.*)All other con', text).group(1)
                if bool(re.search(r'\d\d\d+', match))==True:
                    matches = re.split(r'\s', match)
                    test = [x for x in matches if re.match(r'.*\d(\,|\d).*',x)][0]
                    gov_grants = int(re.sub(r'[^0-9]', "", test))
                else:
                    gov_grants = 0
        elif 'Goverment grants' in text:
            if re.search('Goverment grants(.*)All other con', text)==None:
                gov_grants= np.nan
            else:
                match= re.search('Goverment grants(.*)All other con', text).group(1)
                if bool(re.search(r'\d\d\d+', match))==True:
                    matches = re.split(r'\s', match)
                    test = [x for x in matches if re.match(r'.*\d(\,|\d).*',x)][0]
                    gov_grants = int(re.sub(r'[^0-9]', '', test))
                else:
                    gov_grants = 0
        else:
            gov_grants = np.nan  
        df2 = pd.DataFrame([{'ein': ein, 'tax_year':tax_year, 'gov_grants':gov_grants}])
        df = pd.concat([df, df2])
    print(idx,'/',len(htmls), 'done!')
    name = re.search(r'(.*).zip', zips[idx]).group(1)
    df.to_csv(os.path.join(directory, name+'.csv'))
    shutil.rmtree(newfolder)
print('all done!')
