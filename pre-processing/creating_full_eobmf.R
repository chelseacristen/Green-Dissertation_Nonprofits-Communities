###########################
########################### NCCS DATA
#Install necessary packages:
install.packages("qpcR")


#Naming all the working directories I'll need:
cleaning_nccs_wd <- "your_directory/NCCS_Cleaning/"
clean_nccs_wd <- "your_directory//NCCS_Clean/"
subsets_nccs_wd <- "your_directory//NCCS_Subsets/" 
dedup_nccs_wd <- "your_directory//NCCS_Deduplicated/"


cleaning_nber_wd <- "your_directory//NBER_Cleaning/"
clean_nber_wd <- "your_directory//NBER_Clean/"
subsets_nber_wd <- "your_directory//NBER_Subsets/" 
dedup_nber_wd <- "your_directory//NBER_Deduplicated/"


merged <- "your_directory//Merged"
merged_v2 <- "your_directory//Merged_v2" 


#######CLEANING THE NCCS FILES, SAVING THEM, SUBSETTING THEM, SAVING THEM
#Load the NCCS file:
setwd(cleaning_nccs_wd)


# list all my file names in my working directory
files <- list.files(path=cleaning_nccs_wd)
for (i in 16:length(files)){
  file <- files[i] #Saving the name of the i'th file
  setwd(cleaning_nccs_wd)
test_nccs <- read.csv(files[i])
library(stringr)
date <- paste0(20, as.numeric(str_match(file, "\\d\\d\\d\\d"))) #Saving the date 
#for that i'th file
file_clean <- paste0("clean", file) #Saving the name of that file's clean version 
#(for later)


#Adding a column to the dataset that reflects which version of the EO-BMF it came from
test_nccs$original_file <- paste0('eobmf',date, 'us')
test_nccs$original_file_year <- as.numeric(str_match(date, "\\d\\d\\d\\d"))


#Making the column names for the EO-BMFs lower-case
names(test_nccs) <- tolower(names(test_nccs))


#Subset each dataframe to only U.S. states, no territories:
test_nccs <- test_nccs[test_nccs$state %in% state.abb,]


#Using regular expressions to extract tax year and tax month:
test_nccs$tax_year <- as.numeric(str_match(test_nccs$taxper, "\\d\\d\\d\\d"))
test_nccs$tax_month <- as.numeric(str_sub(test_nccs$taxper, -2, -1))


#EINs are supposed to contain 9 digits. Make sure that all of them do:
test_nccs$ein <- formatC(test_nccs$ein, width = 9, format="d", flag = "0")


#Zipcodes are supposed to contain 5 digits. Make sure that all of them do:
test_nccs$zip5 <- formatC(test_nccs$zip5, width=5, format="d", flag = "0")


#Let's create a variable for test_nccs indicating the source is NCCS or NBER. I will do
#this for NBER sourced datasets too.
test_nccs$source <- "NCCS"


#Change names of NCCS variables to match NBER data:
names(test_nccs)[names(test_nccs) == 'address'] <- 'street'
names(test_nccs)[names(test_nccs) == 'zip5'] <- 'zip'
names(test_nccs)[names(test_nccs) == 'subseccd'] <- 'subsection'
names(test_nccs)[names(test_nccs) == 'fndncd'] <- 'foundation'
names(test_nccs)[names(test_nccs) == 'frcd'] <- 'filing_req_cd' #These have different values for NCCS and NBER though, so that's important. 
names(test_nccs)[names(test_nccs) == 'accper'] <- 'acct_pd'
names(test_nccs)[names(test_nccs) == 'income']<- 'income_amt'
names(test_nccs)[names(test_nccs) == 'assets']<- 'asset_amt'
names(test_nccs)[names(test_nccs) == 'sec_name'] <- 'sort_name'
names(test_nccs)[names(test_nccs) == 'gen'] <- 'group'


#USER_filing_req_cd and USER_pf_filing_req_cd are combined in the NCCS data. 
#Might be worth breaking this into two different variables to match the NBER data.
test_nccs$filing_req_cd_1 <- NA
test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==0] <-  0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==1] <-  0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==10] <-  1
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==11] <-  0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==20] <-  2
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==21] <-  0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==30] <-  3
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==31] <-  0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==40] <-4
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==41] <- 0 
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==60] <-  6
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==61] <-0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==70] <- 7 
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==71] <-0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==130] <-13
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==131] <-0
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==140] <-14
  test_nccs$filing_req_cd_1[test_nccs$filing_req_cd==141] <-0


 test_nccs$pf_filing_req_cd <- NA
test_nccs$filing_req_cd[test_nccs$filing_req_cd==0] <-  0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==1] <- 1  
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==10] <-  0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==11] <-  1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==20] <-  0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==21] <-  1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==30] <-  0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==31] <-  1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==40] <-0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==41] <- 1 
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==60] <-  0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==61] <-1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==70] <- 0 
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==71] <-1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==130] <-0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==131] <-1
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==140] <-0
  test_nccs$pf_filing_req_cd[test_nccs$filing_req_cd==141] <-1


test_nccs$filing_req_cd <- test_nccs$filing_req_cd_1


remove <- "filing_req_cd_1"
test_nccs <- test_nccs[, !names(test_nccs) %in% remove]


#Let's create a ruling_month and ruling_year column for test_nccs
test_nccs$ruledate<- as.numeric(test_nccs$ruledate)
test_nccs$ruling_year <- as.numeric(str_match(test_nccs$ruledate, "\\d\\d\\d\\d"))
test_nccs$ruling_month <- as.numeric(str_sub(test_nccs$ruledate, -2, -1))


#Creating a column name for the source of the data:
test_nccs$source <- "NCCS"


#Eliminated the fipscodes in the NCCS data because I want them to be standardized
#with the NBER data using geo-coding and a spatial join with 2020 Tiger shape files.


keep <- c('ein', 'name', 'street', 'city', 'state', 'zip', 'subsection',
          'ruling_year', 'ruling_month', 'foundation', 'tax_year', 'tax_month',
          'ntee1', 'acct_pd', 'filing_req_cd', 'pf_filing_req_cd', 'asset_amt', 
          'income_amt', 'sort_name', 'ntee1',  'original_file', 'original_file_year',
          'source')


#Keeping only particular variables (ones that NCCS *and* NBER contain) and reordering
#the dataset, all at the same time!
library(dplyr)
test_nccs <- test_nccs %>% select(any_of(keep))


#Write a CSV of the clean full EO-BMF dataset to the working directory containing
#clean files:
setwd(clean_nccs_wd)
write.csv(test_nccs, file=file_clean)
print(paste0(i, " clean file created"))


#Creating subsets for every tax year and state in the NCCS data:
tax_years <- unique(test_nccs$tax_year) #save the unique tax years in the dataset
tax_years <- tax_years[!is.na(tax_years)]
state_names <- unique(test_nccs$state) #save the unique state names in the dataset
state_names <- state_names[!is.na(state_names)]
source <- unique(test_nccs$source) #save the source (NBER/NCCS in the dataset)
eo <- unique(test_nccs$original_file) #save the EOBMF file info in the dataset


setwd(subsets_nccs_wd) #Change the working directory
library(dplyr)


for(i in 1:length(state_names)){ #for every state
  s <- state_names[i] #save the name of the state
  for(j in 1:length(tax_years)){ #for every tax year
    ta <- as.numeric(tax_years[j]) #save the name of the tax year
    #subset the dataset to the specific state and tax year within each 
    #unit of the loop
    sub <- test_nccs%>% filter(state==s & tax_year==ta)
    
    newname <- paste0(ta,s,source,eo,".csv") #create a file name for that unique
    #state and tax year combination
    
    if(nrow(sub)>0){
    write.csv(sub,file=newname)   #write a CSV to my NCCS_Subsets folder for that 
    #state and tax year combination 
    rm(sub) }
    print(paste0(ta,s, "complete"))
  }
}
print(paste0(eo, " subset creation complete"))
rm(test_nccs)
}


#####NOW DOING THE SAME FOR THE NBER DATASET
setwd(cleaning_nber_wd) #Set working directory
#"Cleaning" the NBER data: Making its columns standard with the NCCS data:
#Load the NBER file:


# list all my file names in my working directory
files <- list.files(path=cleaning_nber_wd)


for (i in 1:length(files)){
  file <- files[i] #Saving the name of the i'th file
  
  setwd(cleaning_nber_wd)
  test_nber <- read.csv(files[i])
  
  library(stringr)
  date <- paste0(as.numeric(str_match(file, "\\d\\d\\d\\d"))) #Saving the date 
  #for that i'th file
  file_clean <- paste0("clean", file) #Saving the name of that file's clean version 
  #(for later)
  
  #Let's create a variable for test_nccs indicating the source is NCCS or NBER. I will do
  #this for NBER sourced datasets too.
  #Subset each dataframe to only U.S. states, no territories:
  test_nber <- test_nber[test_nber$state %in% state.abb, ]
  
  #Creating a column that indicates the data source:
  test_nber$source <- "NBER"
 
  keep <- c('ein', 'name', 'street', 'city', 'state', 'zip', 'subsection',
            'ruling_year', 'ruling_month', 'foundation', 'tax_year', 'tax_month',
            'ntee1', 'acct_pd', 'filing_req_cd', 'pf_filing_req_cd', 'asset_amt', 
            'income_amt', 'sort_name', 'ntee1',  'original_file', 'original_file_year', 
            'source')
  
  #Keeping only particular variables (ones that NCCS *and* NBER contain) and reordering
  #the dataset, all at the same time!
  library(dplyr)
  test_nber <- test_nber %>% select(any_of(keep))
  
  #Write a CSV of the clean full EO-BMF dataset to the working directory containing
  #clean files:
  setwd(clean_nber_wd)
  write.csv(test_nber, file=file_clean)
  print(paste0(i, " clean file created"))


  #Write a CSV for every state and tax year: 
  tax_years <- unique(test_nber$tax_year) #save the unique tax years in the dataset
  tax_years <- tax_years[!is.na(tax_years)]
  state_names <- unique(test_nber$state) #save the unique state names in the dataset
  state_names <- state_names[!is.na(state_names)]
    
  source <- unique(test_nber$source) #save the source (NBER/NCCS in the dataset)
  eo <- unique(test_nber$original_file_year) #save the EOBMF file info in the dataset
  
  
  setwd(subsets_nber_wd) #Change the working directory
  for(i in 1:length(state_names)){ #for every state
    s <- state_names[i] #save the name of the state
    for(j in 1:length(tax_years)){ #for every tax year
      ta <- as.numeric(tax_years[j]) #save the name of the tax year
      #subset the dataset to the specific state and tax year within each unit of the loop
      sub <- test_nber %>% filter(state==s & tax_year==ta)
      newname <- paste0(ta,s,source,"eobmf", eo, "us",".csv") #create a file name for that unique
      #state and tax year combination
     
      ##DO THIS ONLY FOR STATE YEAR COMBINATIONS WHERE THE NUMBER OF ROWS IS GREATER
      ##THAN ZERO:
      if(nrow(sub)>0){
       write.csv(sub,file=newname)   #write a CSV to my NBER_Subsets folder for that 
      #state and tax year combination
        rm(sub)}
      print(paste0(ta, s, " complete"))
      
    }
  }
  rm(test_nber)
  print(paste0(source, eo, " subset creation complete"))
}


#############################
######DE-DUPLICATING AMONG THE NCCS AND NBER DATA SETS:
#################
setwd(subsets_nccs_wd)


#Save the unique tax years in my working directory:
all_files <- list.files(path = subsets_nccs_wd)
library(stringr)
all_years <- as.numeric(unique(str_match(all_files, "[0-9]{4}")))


#Save the unique states in my working directory:
all_states <- unique(str_match(all_files, "[A-Z]{2}"))
all_states <- all_states[!is.na(all_states)]


library(data.table)
library(dplyr)


for (i in 1:length(all_years)){
  ta_2 <- all_years[i] #Save the specific year value 
  for(j in 1:length(all_states)){
    s_2 <- all_states[j] #Save the specific state value
    phrase <- paste0(ta_2, s_2)
    
    #Read in the files with that specific state and year value into the global
    #environment
    setwd(subsets_nccs_wd)
    temp = list.files(path=subsets_nccs_wd, pattern=phrase)
    if(length(temp)>0)
    {for (k in 1:length(temp)) assign(temp[k], read.csv(temp[k]))
      
      #Create list of dataframes
      df_list <- mget(ls(pattern = phrase))
      
      #Remove dataframes from global environment
      rm(list = ls(pattern = phrase))
      
      #Row bind list of dataframes
      combined <-  rbindlist(df_list) 
      keep <- c('ein', 'name', 'street', 'city', 'state', 'zip', 'subsection',
                'ruling_year', 'ruling_month', 'foundation', 'tax_year', 'tax_month',
                'ntee1', 'acct_pd', 'filing_req_cd', 'pf_filing_req_cd', 'asset_amt', 
                'income_amt', 'sort_name', 'ntee1')
      
      #Keeping only particular variables (ones that NCCS *and* NBER contain)
      combined <- combined %>% select(any_of(keep))


      
      if(nrow(combined)>0){
      #De-duplicate the files
      combined <- combined[!duplicated(combined),] 
      
      #Assign a CSV name for combined dataframe:
      co_file <- paste0(ta_2, s_2, "NCCS", "joined", ".csv")
      
      #Change working directory:
      setwd(dedup_nccs_wd)
      
      #Write a CSV for the deduplicated, combined file, save to working directory:
      write.csv(combined, file=co_file)
      }
      rm(combined)
      rm(df_list)
    }
    rm(temp)
    print(paste0(s_2, ta_2, " complete")) 
  }
  }           


#De-duplicating NBER files: 
setwd(subsets_nber_wd)


#Save the unique tax years in my working directory:
all_files <- list.files(path = subsets_nber_wd)
library(stringr)
all_years <- as.numeric(unique(str_match(all_files, "[0-9]{4}")))


#Save the unique states in my working directory:
all_states <- unique(str_match(all_files, "[A-Z]{2}"))
all_states <- all_states[!is.na(all_states)]


library(data.table)
library(dplyr)


for (i in 1:length(all_years)){
  ta_2 <- all_years[i] #Save the specific year value 
  for(j in 1:length(all_states)){
    s_2 <- all_states[j] #Save the specific state value
    phrase <- paste0(ta_2, s_2)
    
    #Read in the files with that specific state and year value into the global
    #environment
    setwd(subsets_nber_wd)
    temp = list.files(path=subsets_nber_wd, pattern=phrase)
    if(length(temp)>0)
    {for (k in 1:length(temp)) assign(temp[k], read.csv(temp[k]))
      
      #Create list of dataframes
      df_list <- mget(ls(pattern = phrase))
      
      #Remove dataframes from global environment
      rm(list = ls(pattern = phrase))
      
      #Row bind list of dataframes
      combined <-  rbindlist(df_list) 
      keep <- c('ein', 'name', 'street', 'city', 'state', 'zip', 'subsection',
                'ruling_year', 'ruling_month', 'foundation', 'tax_year', 'tax_month',
                'ntee1', 'acct_pd', 'filing_req_cd', 'pf_filing_req_cd', 'asset_amt', 
                'income_amt', 'sort_name', 'ntee1')
      
      #Keeping only particular variables (ones that NCCS *and* NBER contain)
      combined <- combined %>% select(any_of(keep))
      
      
      if(nrow(combined)>0){
        #De-duplicate the files
        combined <- combined[!duplicated(combined),] 
        
        #Assign a CSV name for combined dataframe:
        co_file <- paste0(ta_2, s_2, "NBER", "joined", ".csv")
        
        #Change working directory:
        setwd(dedup_nber_wd)
        
        #Write a CSV for the deduplicated, combined file, save to working directory:
        write.csv(combined, file=co_file)
      }
      rm(combined)
      rm(df_list)
    }
    rm(temp)
    print(paste0(s_2, ta_2, " complete")) 
  }
}   
#The only duplicated cells truly left here are ones that seem to have more than one
#NTEE encoding. Don't know what to do about that. 


###Matching dataset subsets from NBER and NCCS and deduplicating the files:
#Identify all the files in the NBER subset folder


nber_files <- list.files(path=dedup_nber_wd)
library(stringr)
library(data.table)
nber_dates <- unique(as.numeric(str_match(nber_files, "\\d\\d\\d\\d"))) #Saving the unique 
#years in the NBER files
nber_state_names <- unique(str_match(nber_files, "[A-Z][A-Z]")) #Saving the unique 
#states in the NBER files


#Identify all the files in the NCCS deduplicated folder


  nccs_files <- list.files(path=dedup_nccs_wd)
  nccs_dates <- unique(as.numeric(str_match(nccs_files, "\\d\\d\\d\\d"))) #Saving the unique 
  #years in the NBER files
  nccs_state_names <- unique(str_match(nber_files, "[A-Z][A-Z]")) #Saving the unique 
  #states in the NBER files
  
  full_years <- c(nber_dates, nccs_dates)
  full_years <- unique(full_years)
    
  full_state_names <- c(nber_state_names, nccs_state_names)
    full_state_names <- unique(full_state_names)
  
for (i in 1:length(full_state_names)){
  state_name <- full_state_names[i]
  for(j in 1:length(full_years)){
  year <- full_years[j]
  newname <- paste0(year,state_name,"merged.csv")
  
    setwd(dedup_nber_wd)
    #If the NBER subset folder contains a file with the year and state name in 
    #this loop
    start <- paste0(year, state_name)
    temp = list.files(path=dedup_nber_wd, pattern=start)
    
    #Read those files into the global environment
    if(length(temp)>0)
    {for (k in 1:length(temp)) assign(temp[k], read.csv(temp[k]))}
     
    #If the NCCS subset folder contains a file with the year and state name in 
    #this loop 
    setwd(dedup_nccs_wd)
    temp = list.files(path=dedup_nccs_wd, pattern=start)
    
    #Read those files into the global environment
    if(length(temp)>0)
    {for (k in 1:length(temp)) assign(temp[k], read.csv(temp[k]))}
    
    #Create list of dataframes now in the global environment
    df_list <- mget(ls(pattern = start))
    #Remove the dataframes themselves from global environment
    if (length(df_list)>0)
    {rm(list = ls(pattern = start))


    #Row bind list of dataframes
    combined <-  rbindlist(df_list)
    combined <- combined[!duplicated(combined), ]
    
    #Set working directory for saving fully merged NCCS/NBER file:
    setwd(merged)
    if(nrow(combined)>0)
    {combined <- combined %>% select(any_of(keep))
      write.csv(combined, file=newname)
      rm(combined)}
    }
    
    print(paste0(newname," complete"))
    rm(df_list)
  }
}


###Let's go back into those merged files and deduplicate *again*. That is, some
#rows seem to have the same tax ID and tax year, but with slight variations in 
#column entries.
setwd(merged)
library(dplyr)
library(stringr)
set.seed(98144)
    
all_files <- list.files(path = merged)
for (i in 1:length(all_files)){
    setwd(merged)
    file <- read.csv(all_files[i])
      
    eins <- unique(file$ein)#Save list of unique tax IDs in the file
    tax_year <- unique(file$tax_year)#Save unique tax year in the file
    state_name <- unique(file$state) #Save state name in the file
      
    dup <- file %>% group_by(ein) %>% summarise(n()) %>% 
      filter(`n()`>1) %>% select(ein) #extracting duplicated eins
      
    if(nrow(dup)>0){
      #Saving one version of the file with duplicated EINs:
    file2 <- file[file$ein %in% dup$ein, ]
      
      #Saving the other version of the file with *no* duplicated EINs:
    file <- file[!(file$ein %in% dup$ein), ]
      
    file2$na_count <- rowSums( is.na( file2[,])) #count the number of NAs
    file2 <- file2 %>% group_by(ein) %>% slice_min(na_count)
    file2 <- file2 %>% group_by(ein) %>% slice_sample(n=1)
      
      #Remove the na_count column 
    file2 <- file2 %>% select(!(na_count))
      
      #Bind the newly saved row to the original data, now ready to receive that EIN and
      #tax year combination
    file <- rbind(file, file2)
      }
      
    setwd(merged_v2)
    newname <- paste0(tax_year, state_name, "merged_v2.csv")
    write.csv(file, newname)
    print(paste0(all_files[i], " remerged"))
    }

##############################################
###STUFF TO DO IN NBER DATA:
#Omit these variables from the NBER data
#Set working directory: 
set_wd(cleaning_wd)


omit_vars <- c("ntee1num","ntee1_3num", "activity1", "activity2",
               "ntee1_3", "ntee_cd", 'affiliation', "subaffil",
               'status', 'X', 'revenue_amt', 'ico', 'classification', 
               'organization', 'deductibility', 'advrule', 'tax_period',
               'asset_cd', 'income_cd')
AL <- AL[,!(colnames(AL) %in% omit_vars)]


#Make changes to the combined nccs dataset for conformity to NBER (One last change!)
combined_nccs <- combined_nccs[,-1] #Delete the first column of combined nccs 
combined_nccs$source <- "NBER"
names(combined_nccs)


setwd(cleaning_nccs_wd) #Set working directory


# list all my file names in my working directory
files <- list.files(path=cleaning_nccs_wd)


#Creating a loop over all of those files to save their column names
#and then determine which of them have different column names:
for (i in 1:length(files)){
  nccs <- read.csv(files[i])
  vecs <- paste0("vec", i)
  assign(vecs, colnames(nccs))
  rm(nccs)
  print(i)
}
rm(vecs)


library("qpcR")
nccs_colnames <- "vec"
vec_list <- mget(ls(pattern = nccs_colnames))


#De-duplicate 
vec_listd <- vec_list[!duplicated(vec_list)]
length(vec_listd$vec1)
length(vec_listd$vec18) 
length(vec_listd$vec21)
length(vec_listd$vec37)
length(vec_listd$vec40)


setdiff(vec_listd$vec1, vec_listd$vec39)


#Looks like vec18 is 49 columns, then vec19 and vec20 are 48 columns, and vec21 
#and beyond are 49 columns. What are those column name differences?
setdiff(vec18, vec19)
#fipsold is the only difference. 
#Otherwise, it looks like the ordering is simply different on these datasets, and 
#some of the datasets later on have more variables than earlier versions. Otherwise,
#these all look super similar. What will address these differences?
#1. Make sure fipsold is dropped as a variable from an NCCS dataset if it contains it.
#2. Make sure to order all variables in a standard manner (the loop does that)


#Wow, looks like we have some files that do not contain real years (specifically
#the values 1090 and NA)
#Manually deleting them from the working directory


#Now removing the old list of files
rm(all_files)


#Let's list the full set of files once again, now that the invalid docs have been
#deleted:
all_files <- list.files(path = subsets_nccs_wd)




###Removing three columns: original file, original file year, and source in 
#order to facilitate proper deduplication among NCCS files and then between
#NCCS and NBER files. Also removing 'group', if it exists.
vars2 <- c('original_file', 'original_file_year', 'source')


