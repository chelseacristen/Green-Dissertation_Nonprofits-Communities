#Set your working directory:

##################################
#pub78 was last updated on March 14, 2022
pub78 <- read_table("pub78.txt", header = FALSE, sep = "|", dec = ".")
head(pub78)
View(pub78)
#Okay, so R is chopping off the zeros from the front. Have to fix that!
col.names(pub78) <- c("ein", "org_name", "city", "state", "country", 
                      "deduct_code")


#See this page for the deductibility status codes: 
#https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-deductibility-status-codes
####################################


#######CREATING FULL EIN-FILING YEAR DATASETS FOR TAX EXEMPT ORGS
install.packages("readxl")
library("readxl")


#Not all of these files have the same formats, so I'm going to 
#separate these below by filing type


##########LOADING IN EZs first: processed from 2012 to April 13, 2022:

ez_20<- read_excel("20eoextractez.xlsx")
ez_19 <- read_excel("19eoextractez.xlsx")
ez_18 <- read_excel("18eoextractez.xlsx")


#Let's make sure these files have the same column names before joining them
colnamesez20<- colnames(ez_20)
colnamesez19<- colnames(ez_19)
colnamesez18<- colnames(ez_18)
setdiff(colnamesez19, colnamesez20)
names(ez_20)[names(ez_20) == 'e-file'] <- 'elf'
colnamesez20<- colnames(ez_20)
#The column names for EZ 2019 and 2020 are now the same


#Checking all the column names btw EZ 2019 and 2018 to make sure
#they are substantively the same
setdiff(colnamesez18, colnamesez19)
setdiff(colnamesez19, colnamesez18)
#They are! I'm going to make all the column names from EZ 2018 the 
#same as those from EZ 2019 now
names(ez_18) <- colnamesez19
colnamesez18<- colnames(ez_18)
setdiff(colnamesez18, colnamesez19)
#Great, and now 2018, 2019, and 2020 column names are the same!


#Check to make sure these .dat files loaded correctly:
install.packages("readr")
library(readr)


ez_17 <- read_table("17eofinextractEZ.dat")
ez_16 <- read_table("16eofinextractez.dat")
ez_15 <- read_table("15eofinextractEZ.dat")
ez_14 <- read_table("14eoextractez.dat")
ez_13 <- read_table("13eoextractez.dat")
ez_12 <- read_table("12eoextractez.dat")


#Okay, they all loaded! Looks like ez_12 has 40 variables, and ezs
#13 and 14 have 71 variables. Let's see whether the other files
#have the same column names
colnamesez17<- colnames(ez_17)
colnamesez16<- colnames(ez_16)
colnamesez15<- colnames(ez_15)
colnamesez14<- colnames(ez_14)
colnamesez13<- colnames(ez_13)
colnamesez12<- colnames(ez_12)
setdiff(colnamesez17, colnamesez18)
setdiff(colnamesez18, colnamesez17)
setdiff(colnamesez17, colnamesez16)
setdiff(colnamesez16, colnamesez17)
setdiff(colnamesez15, colnamesez18)
setdiff(colnamesez18, colnamesez15)


#Spot checking these differences in the documentation to see if there were
#substantive changes. Looks like 2015, 2016, and 2017 are the same as the others, so
#we will give them the same column names as 2018, 2019, and 2020!
names(ez_17) <- names(ez_18)
names(ez_16) <- names(ez_18)
names(ez_15) <- names(ez_18)
colnamesez17<- colnames(ez_17)
colnamesez16<- colnames(ez_16)
colnamesez15<- colnames(ez_15)


#Now let's see what the situation is with 2013 and 2014, which only have 71
#columns
colnamesez13
colnamesez12
#Looks like they simply didn't have the e-file option! Creating a new column 
#for them with e-file = 0 for every row.
ez_13$elf <- 0
ez_14$elf <- 0 
#Making that column the first column now
ez_13 <- ez_13[ , c("elf",    # Reorder data frame
                       names(ez_13)[names(ez_13) != "elf"])]


ez_14 <- ez_14[ , c("elf",    # Reorder data frame
                    names(ez_14)[names(ez_14) != "elf"])]
colnamesez14<- colnames(ez_14)
colnamesez13<- colnames(ez_13)


#Now checking once again to see substantively whether the columns remain the same
#across the different datasets
setdiff(colnamesez14, colnamesez15)
setdiff(colnamesez15, colnamesez14) #They are!
names(ez_14) <- names(ez_15)
colnamesez14<- colnames(ez_14)
setdiff(colnamesez13, colnamesez14) #And EZ_2013 already shares the same column 
#names as the rest, so we are set! 


#Adding a column to each csv that reflects which version of the IRS EZ file it came from
ez_12$original_file <- 'ez_12'
ez_13$original_file <- 'ez_13'
ez_14$original_file <- 'ez_14'
ez_15$original_file <- 'ez_15'
ez_16$original_file <- 'ez_16'
ez_17$original_file <- 'ez_17'
ez_18$original_file <- 'ez_18'
ez_19$original_file <- 'ez_19'
ez_20$original_file <- 'ez_20'


##NOW MAKING ONE EIN-FILING LEVEL DATASET FOR EZs from 2013-2020:
ez_1320 <- rbind(ez_13, ez_14, ez_15, ez_16, ez_17, ez_18, ez_19, ez_20)
nrow(ez_1320)
rm(ez_13)
rm(ez_14)
rm(ez_15)
rm(ez_16)
rm(ez_17)
rm(ez_18)
rm(ez_19)
rm(ez_20)


#Exporting a csv for all EZs:
write_csv(ez_1320, path = "ez_1320.csv")


#Because 2012 simply has a LOT less columns, I will make another csv that includes only the columns that 2012 contains, but for 2012 to 2020:
setdiff(names(ez_12), names(ez_1320))
setdiff(names(ez_1320), names(ez_12)) #Changing the column names of EIN and tax_prd for 2012:
names(ez_1320)[names(ez_1320) == 'EIN'] <- 'ein'
names(ez_12)[names(ez_12) == 'tax_prd'] <- 'tax_pd'
names(ez_12)[names(ez_12) == 'gftgrntrcvd170'] <- 'gftgrntsrcvd170'
names(ez_12)[names(ez_12) == 'grsrcptsrelatd170'] <- 'grsrcptsrelated170'
names(ez_12)[names(ez_12) == 'grsrcptsadmiss509'] <- 'grsrcptsadmissn509'


setdiff(names(ez_12), names(ez_1320)) 
ez_1320_efficient <- ez_1320[,names(ez_12)]
ez_1220_efficient <- rbind(ez_12, ez_1320_efficient)


write_csv(ez_1220_efficient, path="ez_1220_efficient.csv")


#LOADING IN Regular 990s: processed from 2012 to April 13, 2022:
reg990_20<- read_excel("20eoextract990.xlsx")
reg990_19 <- read_excel("19eoextract990.xlsx")
ncol(reg990_20)
ncol(reg990_19)
colnames(reg990_20) #Looks like I can remove columns 247-251 because they are just empty cells
reg990_20<- reg990_20[,c(1:246)]
ncol(reg990_20)
colnames(reg990_20)
colnames_20<- colnames(reg990_20)
colnames_19<- colnames(reg990_19)
setdiff(colnames_19, colnames_20)
setdiff(colnames_20, colnames_19)
#Standarizing column names
names(reg990_20) <- names(reg990_19)
colnames_20<- colnames(reg990_20)
colnames_19<- colnames(reg990_19)
setdiff(colnames_19, colnames_20)
#Giving them columns to indicate which file each was originally downloaded from:
reg990_20$original_file <- 'reg990_20'
reg990_19$original_file <- 'reg990_19'


#Combining the two files:
full_reg <- rbind(reg990_19, reg990_20)
nrow(full_reg)
nrow(reg990_20) + nrow(reg990_19) #Done!
#Exporting that as a csv for now:

install.packages("readr")
library(readr)
write_csv(full_reg, path= "full_reg.csv") #This looks good!


#clearing some global environment space:
rm(reg990_20)
rm(reg990_19)


reg990_18 <- read_excel("18eoextract990.xlsx")
ncol(reg990_18)
colnames_18 <- names(reg990_18)


#Giving them columns to indicate which file each was originally downloaded from:
reg990_18$original_file <- 'reg990_18'
setdiff(colnames_19, colnames_18) #same column names! Let's rbind again:
full_reg <- rbind(reg990_18, full_reg)


#clearing some global environment space:
rm(reg990_18)




#Check to make sure these .dat files loaded correctly:
reg990_17 <- read_table("17eoextract990.dat")
ncol(reg990_17)
setdiff(colnames(full_reg), colnames(reg990_17))
setdiff(colnames(reg990_17), colnames(full_reg)) #only ein name is different
#Standardizing names
names(reg990_17)<- names(full_reg)
setdiff(colnames(full_reg), colnames(reg990_17)) #all set! Time to rbind:


#Giving them columns to indicate which file each was originally downloaded from:
reg990_17$original_file <- 'reg990_17'
full_reg<- rbind(reg990_17, full_reg)


#Clearing some global environment space:
rm(reg990_17)


reg990_16 <- read_table("16eoextract990.dat")
ncol(reg990_16)
setdiff(colnames(full_reg), colnames(reg990_16))
setdiff(colnames(reg990_16), colnames(full_reg)) #only ein name is different
#standardizing names
names(reg990_16) <- names(full_reg)
setdiff(colnames(full_reg), colnames(reg990_16)) #all set! Time to rbind:


#Giving them columns to indicate which file each was originally downloaded from:
reg990_16$original_file <- 'reg990_16'
full_reg<- rbind(reg990_16, full_reg)






#Clearing some global environment space:
rm(reg990_16)


reg990_15 <- read_table("15eoextract990.dat")
ncol(reg990_15)
setdiff(names(full_reg), names(reg990_15))
setdiff(names(reg990_15), names(full_reg)) #okay, the names are different but content is substantively the same
names(reg990_15) <- names(full_reg)
#Giving them columns to indicate which file each was originally downloaded from:
reg990_15$original_file <- 'reg990_15'
setdiff(names(full_reg), names(reg990_15)) #Time to rbind!


full_reg <- rbind(reg990_15, full_reg)


rm(reg990_15)


reg990_14 <- read_table("14eoextract990.dat")
ncol(reg990_14) #uh oh -it's missing a column! Let's see what it is
setdiff(names(full_reg), names(reg990_14)) 
setdiff(names(reg990_14), names(full_reg)) #Ah, looks like 2014 did not have an efile option! Adding a column to the 2014 dataset titled elf, all containing zeroes:
reg990_14$elf <- 0
#Making that column the first column now
reg990_14 <- reg990_14[ , c("elf", names(reg990_14)[names(reg990_14) != "elf"])]
setdiff(names(full_reg), names(reg990_14)) 
setdiff(names(reg990_14), names(full_reg)) #Perfect, now standardizing names:
names(reg990_14) <- names(full_reg) 
setdiff(names(full_reg), names(reg990_14)) #Time to rbind!
#Giving them columns to indicate which file each was originally downloaded from:
reg990_14$original_file <- 'reg990_14'
full_reg <- rbind(reg990_14, full_reg)


rm(reg990_14)


reg990_13 <- read_table("13eoextract990.dat")
ncol(reg990_13)
setdiff(names(full_reg), names(reg990_13)) 
setdiff(names(reg990_13), names(full_reg)) #Same thing - didn't efile in 2013! Adding a column to the 2014 dataset titled elf, all containing zeroes:
reg990_13$elf <- 0
#Making that column the first column now
reg990_13 <- reg990_13[ , c("elf", names(reg990_13)[names(reg990_13) != "elf"])]
setdiff(names(full_reg), names(reg990_13)) 
setdiff(names(reg990_13), names(full_reg)) 
names(reg990_13) <- names(full_reg)


setdiff(names(full_reg), names(reg990_13)) #Time to rbind!
#Giving them columns to indicate which file each was originally downloaded from:
reg990_13$original_file <- 'reg990_13'
full_reg <- rbind(reg990_13, full_reg)


write_csv(full_reg, path="full_reg.csv")
rm(reg990_13)


reg990_12 <- read_table("12eoextract990.dat")
ncol(reg990_12) #2012 contains WAY less columns. 
setdiff(names(reg990_12), names(full_reg))  #Looks like only EIN and tax_prd need to be renamed
names(reg990_12)[names(reg990_12) == 'EIN'] <- 'ein'
names(reg990_12)[names(reg990_12) == 'tax_prd'] <- 'tax_pd'
#Giving them columns to indicate which file each was originally downloaded from:
reg990_12$original_file <- 'reg990_12'
#Done! Okay. Now let's create a subset of full_reg that only includes column names available in the 2012 file:


full_reg_efficient<- full_reg[, names(reg990_12)]
names(full_reg_efficient)
ncol(full_reg_efficient)
ncol(reg990_12)


setdiff(names(full_reg_efficient), names(reg990_12)) #Time to rbind!
final_n <- nrow(full_reg_efficient) + nrow(reg990_12)
final_n
full_reg_efficient <- rbind(reg990_12, full_reg_efficient)
nrow(full_reg_efficient)
write_csv(full_reg_efficient, path="full_reg_efficient.csv")
rm(reg990_12)




###COMBINING THE EZs and REGULAR 990S INTO ONE LARGE DATAFRAME:
setdiff(names(full_reg_efficient), names(ez_1220_efficient))
setdiff(names(ez_1220_efficient), names(full_reg_efficient)) #Need to figure out which of these columns are actually functionally the same. Exporting the column names now for later documentation review:
reg990 <- names(full_reg_efficient)
ez <- names(ez_1220_efficient)
names_comp <- seq(max(length(reg990), length(ez)))
names_comp <- data.frame(reg990[names_comp], ez[names_comp])
write_csv(names_comp, path="names_comp.csv")


#######Loading in the EO-BMFs from the NBER Repository at the following link:
#https://data.nber.org/tax-stats/population/eo-bmf/
setwd("C:/Users/chg244/Downloads/eobmf")


install.packages("readr")
library(readr)
#load in every EO-BMF, rbind them all, and then de-duplicate the file. 
eobmf201310us <- read.csv("eobmf201310us.csv")
eobmf201403us <- read.csv("eobmf201403us.csv")
eobmf201612us <- read.csv("eobmf201612us.csv")
eobmf201702us <- read.csv("eobmf201702us.csv")
eobmf201703us <- read.csv("eobmf201703us.csv")


#Adding a column to each csv that reflects which version of the EO-BMF it came from
eobmf201310us$original_file <- 'eobmf201310us'
eobmf201403us$original_file <- 'eobmf201403us'
eobmf201612us$original_file <- 'eobmf201612us'
eobmf201702us$original_file <- 'eobmf201702us'
eobmf201703us$original_file <- 'eobmf201703us'




setdiff(names(eobmf201703us), names(eobmf201702us)) #no difference
setdiff(names(eobmf201703us), names(eobmf201612us)) #no difference
setdiff(names(eobmf201703us), names(eobmf201403us))
setdiff(names(eobmf201403us), names(eobmf201703us)) #a lot of the column names are different. Need to make sure these are the same.
setdiff(names(eobmf201403us), names(eobmf201310us)) #2013 and 2014 files are the same though! 


# Let's combine 2013 and 2014 files for now: 
eobmf_1314<- rbind(eobmf201310us , eobmf201403us) 
#De-deduplicate:
eobmf_1314 <- eobmf_1314[!duplicated(eobmf_1314),]
write_csv(eobmf_1314, file="eobmf_1314.csv")


eobmf201704us <- read.csv("eobmf201704us.csv")
eobmf201705us <- read.csv("eobmf201705us.csv")
eobmf201706us <- read.csv("eobmf201706us.csv")
eobmf201707us <- read.csv("eobmf201707us.csv")
#Adding a column to each csv that reflects which version of the EO-BMF it came from
eobmf201704us$original_file <- 'eobmf201704us'
eobmf201705us$original_file <- 'eobmf201705us'
eobmf201706us$original_file <- 'eobmf201706us'
eobmf201707us$original_file <- 'eobmf201707us'


setdiff(names(eobmf201703us), names(eobmf201704us)) #no difference
setdiff(names(eobmf201703us), names(eobmf201705us)) #no difference
setdiff(names(eobmf201703us), names(eobmf201706us)) #no difference
setdiff(names(eobmf201703us), names(eobmf201707us)) #no difference


#Combining 2017-02 files with all files through 2017-07
eobmf20170207<- rbind(eobmf201702us, eobmf201703us, eobmf201704us, eobmf201705us, eobmf201706us, eobmf201707us)
nrow(eobmf20170207)
eobmf20170207 <- eobmf20170207[!duplicated(eobmf20170207),]
nrow(eobmf20170207)
write_csv(eobmf20170207, file="eobmf20170207.csv")


eobmf201708us <- read.csv("eobmf201708us.csv")
eobmf201709us <- read.csv("eobmf201709us.csv")
eobmf201710us <- read.csv("eobmf201710us.csv")
eobmf201711us <- read.csv("eobmf201711us.csv")
eobmf201712us <- read.csv("eobmf201712us.csv")
eobmf201802us <- read.csv("eobmf201802us.csv")
eobmf201803us <- read.csv("eobmf201803us.csv")
eobmf201804us <- read.csv("eobmf201804us.csv")


#Adding a column to each csv that reflects which version of the EO-BMF it came from
eobmf201708us$original_file <- 'eobmf201708us'
eobmf201709us$original_file <- 'eobmf201709us'
eobmf201710us$original_file <- 'eobmf201710us'
eobmf201711us$original_file <- 'eobmf201711us'
eobmf201712us$original_file <- 'eobmf201712us'
eobmf201802us$original_file <- 'eobmf201802us'
eobmf201803us$original_file <- 'eobmf201803us'
eobmf201804us$original_file <- 'eobmf201804us'


setdiff(names(eobmf20170207), names(eobmf201708us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201709us)) #no  difference
setdiff(names(eobmf20170207), names(eobmf201710us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201711us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201712us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201802us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201803us)) #no difference
setdiff(names(eobmf20170207), names(eobmf201804us)) #no difference


#Combining 2017-02 files with all files through 2018-04
eobmf201702201804 <- rbind(eobmf20170207, eobmf201708us, eobmf201709us, eobmf201710us, eobmf201711us, eobmf201712us, eobmf201802us, eobmf201803us, eobmf201804us)
nrow(eobmf201702201804)
eobmf201702201804 <- eobmf201702201804[!duplicated(eobmf201702201804),]
nrow(eobmf201702201804)
write_csv(eobmf201702201804, file="eobmf201702201804.csv")


eobmf201805us <- read.csv("eobmf201805us.csv")
eobmf201806us <- read.csv("eobmf201806us.csv")
eobmf201807us <- read.csv("eobmf201807us.csv")
eobmf201808us <- read.csv("eobmf201808us.csv")
eobmf201809us <- read.csv("eobmf201809us.csv")
eobmf201810us <- read.csv("eobmf201810us.csv")
eobmf201811us <- read.csv("eobmf201811us.csv")
eobmf201812us <- read.csv("eobmf201812us.csv")
eobmf201902us <- read.csv("eobmf201902us.csv")
eobmf201903us <- read.csv("eobmf201903us.csv")
eobmf201904us <- read.csv("eobmf201904us.csv")


#Adding a column to each csv that reflects which version of the EO-BMF it came from
eobmf201805us$original_file <- 'eobmf201805us'
eobmf201806us$original_file <- 'eobmf201806us'
eobmf201807us$original_file <- 'eobmf201807us'
eobmf201808us$original_file <- 'eobmf201808us'
eobmf201809us$original_file <- 'eobmf201809us'
eobmf201810us$original_file <- 'eobmf201810us'
eobmf201811us$original_file <- 'eobmf201811us'
eobmf201812us$original_file <- 'eobmf201812us'
eobmf201902us$original_file <- 'eobmf201902us'
eobmf201903us$original_file <- 'eobmf201903us'
eobmf201904us$original_file <- 'eobmf201904us'


setdiff(names(eobmf201702201804), names(eobmf201805us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201806us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201807us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201808us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201809us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201810us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201811us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201812us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201902us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201903us)) #no difference
setdiff(names(eobmf201702201804), names(eobmf201904us)) #no difference


#Combining 2017-02 files with all files through 2019-04
eobmf201702201904 <- rbind(eobmf201702201804, eobmf201805us, eobmf201806us, eobmf201807us, eobmf201808us, eobmf201809us, eobmf201810us, eobmf201811us, eobmf201812us, eobmf201902us, eobmf201903us, eobmf201904us )
nrow(eobmf201702201904)
eobmf201702201904 <- eobmf201702201904[!duplicated(eobmf201702201904), ]
nrow(eobmf201702201904)
write_csv(eobmf201702201904, path="eobmf201702201904.csv")


#How many objects are in my environment right now?
ls(envir=.GlobalEnv)
#Clearing some extra items: 
rm(list= c())


#Downloading the most recent EO-BMF (date downloaded from IRS website: all regions)
#Merge on EIN/ein tax_pd/tax_prd 
eo1 <- read_csv("eo1.csv")
eo2 <- read_csv("eo2.csv")
eo3 <- read_csv("eo3.csv")
eo4 <- read_csv("eo4.csv")
setdiff(names(eo1), names(eo2)) #no difference
setdiff(names(eo1), names(eo3)) #no difference
setdiff(names(eo1), names(eo4)) #no difference
eobmf202204us <- rbind(eo1, eo2, eo3, eo4)


#Adding a column to each csv that reflects which version of the EO-BMF it came from
eobmf202204us $original_file <- 'eobmf202204us'


write_csv(eobmf202204us, path="eobmf202204us.csv")


setdiff(names(eobmf201702201904), names(eobmf202204us)) #looks like the 2022 file may be all caps for the same variables
setdiff(names(eobmf202204us), names(eobmf201702201904)) #Okay, looks like the older EO-BMF files have more variables than the new 2022 files:
ncol(eobmf202204us)
ncol(eobmf201702201904)


####First thing: make the column names for EO-BMF 2022 lower-case
names(eobmf202204us) <- tolower(names(eobmf202204us))
names(eobmf202204us) #Done! Now let's add columns with the names from the 2013-2019 data to the 2022 EO-BMF:
setdiff(names(eobmf201702201904), names(eobmf202204us))


unique(eobmf202204us$tax_period) 
install.packages("stringr")
library(stringr)


#Using regular expressions to extract tax year and tax month:
eobmf202204us$tax_year <- as.numeric(str_match(eobmf202204us$tax_period, "\\d\\d\\d\\d"))
eobmf202204us$tax_month <- as.numeric(str_sub(eobmf202204us$tax_period, -2, -1))
#Checking to make sure this worked:
unique(eobmf202204us$tax_year)
unique(eobmf202204us$tax_month) #It worked! 


eobmf202204us$ntee1 <- NA
eobmf202204us$ntee1_3 <- NA
eobmf202204us$subaffil <- NA
eobmf202204us$ntee1num <- NA
eobmf202204us$ntee1_3num <- NA


setdiff(names(eobmf202204us), names(eobmf201702201904)) #These two are ready to join now!


eobmf201702202204 <- rbind(eobmf201702201904, eobmf202204us)
eobmf201702202204 <- eobmf201702202204[!duplicated(eobmf201702202204), ]
nrow(eobmf201702202204)
write_csv(eobmf201702202204, path= "eobmf201702202204.csv")


#How many objects are in my environment right now?
ls(envir=.GlobalEnv)
#Clearing some extra items: 
rm(list= c("eo1" ,              "eo2"     ,          "eo3"      ,        
 "eo4"         ,            "eobmf201310us"   , 
"eobmf201403us"   ,  "eobmf201612us"   ,  "eobmf20170207"  ,  
"eobmf201702201804", "eobmf201702201904" ,
"eobmf201702us"  ,   "eobmf201703us"  ,   "eobmf201704us" ,   
"eobmf201705us"  ,   "eobmf201706us"  ,   "eobmf201707us"  ,  
"eobmf201708us"  ,   "eobmf201709us"  ,   "eobmf201710us"  ,  
"eobmf201711us"  ,   "eobmf201712us"  ,   "eobmf201802us"  ,  
"eobmf201803us"  ,   "eobmf201804us"  ,   "eobmf201805us"  ,  
"eobmf201806us"  ,   "eobmf201807us"  ,   "eobmf201808us"  ,  
"eobmf201809us"  ,   "eobmf201810us"  ,   "eobmf201811us"  ,  
"eobmf201812us"  ,   "eobmf201902us"  ,   "eobmf201903us"  ,  
"eobmf201904us" ,    "eobmf202204us" ))


#Okay, so let's see if we can't merge EO-BMFs from 2013 and 2014 in with all of this: (I checked the EO-BMF 2013/2014 in excel and it looks like ein is in fact included, which means I should be able to)
eobmf201702202204 <- read_csv("eobmf201702202204.csv")
eobmf_1314 <- read_csv("eobmf_1314.csv")
ncol(eobmf_1314)
ncol(eobmf201702202204) #okay, these have different numbers of columns. Let's figure out what's going on here.
setdiff(names(eobmf_1314), names(eobmf201702202204))
setdiff(names(eobmf201702202204), names(eobmf_1314)) #Changing the names of eo_1314 to be consistent with eobmf201702202204 names that mean the same thing
names(eobmf_1314)[names(eobmf_1314) == 'orgname'] <- 'name'
names(eobmf_1314)[names(eobmf_1314) == 'namecare'] <- 'ico'
names(eobmf_1314)[names(eobmf_1314) == 'address'] <- 'street'
names(eobmf_1314)[names(eobmf_1314) == 'zipcode'] <- 'zip'
names(eobmf_1314)[names(eobmf_1314) == 'stabbrev'] <- 'state'
names(eobmf_1314)[names(eobmf_1314) == 'sortname'] <- 'sort_name'
names(eobmf_1314)[names(eobmf_1314) == 'tax_prd'] <- 'tax_period'
names(eobmf_1314)[names(eobmf_1314) == 'affil'] <- 'affiliation'
names(eobmf_1314)[names(eobmf_1314) == 'assetamt'] <- 'asset_amt'
names(eobmf_1314)[names(eobmf_1314) == 'incomeamt'] <- 'income_amt'
names(eobmf_1314)[names(eobmf_1314) == 'class'] <- 'classification'
names(eobmf_1314)[names(eobmf_1314) == 'pffilreqcd'] <- 'pf_filing_req_cd'
names(eobmf_1314)[names(eobmf_1314) == 'acc_prd'] <- 'acct_pd'
names(eobmf_1314)[names(eobmf_1314) == 'filreqcd'] <- 'filing_req_cd'
names(eobmf_1314)[names(eobmf_1314) == 'deduct'] <- 'deductibility'
names(eobmf_1314)[names(eobmf_1314) == 'found'] <- 'foundation'
names(eobmf_1314)[names(eobmf_1314) == 'incomecd'] <- 'income_cd'
eobmf201702202204$group <- as.numeric(eobmf201702202204$group) #Make this consistent with EO-BMF
names(eobmf_1314)[names(eobmf_1314) == 'grexemp'] <- 'group'
names(eobmf_1314)[names(eobmf_1314) == 'orgcode'] <- 'organization'
names(eobmf_1314)[names(eobmf_1314) == 'asset'] <- 'asset_cd'
names(eobmf_1314)[names(eobmf_1314) == 'ntee'] <- 'ntee_cd'
names(eobmf_1314)[names(eobmf_1314) == 'f990revamt'] <- 'revenue_amt'
names(eobmf201702202204)[names(eobmf201702202204) == 'activity'] <- 'activity1' #only one activity code available in eobmf201702202204. Adding a blank activity2 column to eobmf201702202204
eobmf201702202204$activity2 <- NA
names(eobmf_1314)[names(eobmf_1314) == 'exempt'] <- 'status'


unique(eobmf_1314$rulingdt) #This doesn't seem to mean anything, with values of "NA" and "0" Removing these from the eobmf_1314 dataset:
remove <- "rulingdt"
eobmf_1314 <- eobmf_1314[,!(colnames(eobmf_1314) %in% remove)]


unique(eobmf201702202204$ruling)
unique(eobmf_1314$ruling_year)
#Let's create a ruling_month and ruling_year column for eobmf201702202204
eobmf201702202204$ruling<- as.numeric(eobmf201702202204$ruling)
eobmf201702202204$ruling_year <- as.numeric(str_match(eobmf201702202204 $ruling, "\\d\\d\\d\\d"))
eobmf201702202204$ruling_month <- as.numeric(str_sub(eobmf201702202204 $ruling, -2, -1))


remove <- "ruling"
eobmf201702202204 <- eobmf201702202204[,!(colnames(eobmf201702202204) %in% remove)]


#Looks like negative signs are already incorporated into income  and revenue amounts for EO BMF 2013/2014
names(eobmf_1314)[names(eobmf_1314) == 'incomeamt'] <- 'income_amt'
negative<- eobmf_1314$income_amt[eobmf_1314$income_amt<0]
unique(negative)


#Looks like revenue_amt already incorporates negative values.
names(eobmf_1314)[names(eobmf_1314) == 'f990revamt'] <- 'revenue_amt'
negative<- eobmf_1314$revenue_amt[eobmf_1314$revenue_amt <0]
unique(negative)
a <- which(eobmf_1314$revenue_amt <0)
b <- which(eobmf_1314$f990revneg =="-")
setdiff(a, b)


#This means we can drop the incomeneg and f990revneg from the eobmf_1314 file
remove <- c("f990revneg", "incomeneg")
eobmf_1314 <- eobmf_1314[,!(colnames(eobmf_1314) %in% remove)]
names(eobmf_1314)


#Just checking: EO BMF 2017-2022 does in fact also include income and revenue amounts with negative values. Cool! 
a <- eobmf201702202204$revenue_amt[eobmf201702202204$revenue_amt<0]
unique(a)


b <- eobmf201702202204$income_amt[eobmf201702202204$income_amt <0]
unique(b)


unique(eobmf_1314$exempt)


#Creating an advance ruling expiration date column in eobmf201702202204 filled with NA
eobmf201702202204$advrule <- NA


##Time to combine eobmf_1314 and eobmf201702202204!
full_eobmf <- rbind(eobmf_1314, eobmf201702202204)
full_eobmf <- full_eobmf[!duplicated(full_eobmf), ]
full_eobmf$original_file_year <- as.numeric(str_match(full_eobmf$original_file, "\\d\\d\\d\\d"))
unique(full_eobmf$original_file_year)
 
nrow(full_eobmf)
write_csv(full_eobmf, path= "full_eobmf.csv")


rm(list=c("eobmf201702202204", "eobmf_1314"))


##WOW. It's 9.62 GB!! That's crazy. 


#####Okay! Now merging financial 990 data and the EO-BMF data 
##Starting with the EZs from 2012-2020
x <- full_eobmf
y <- read_csv("ez_1220_efficient.csv")
names(x)
names(y)
#Rename full_eobmf column tax_period to tax_pd
names(x)[names(x) == 'tax_period'] <- 'tax_pd'
typeof(x$tax_pd)
typeof(y$tax_pd)
typeof(x$ein)
typeof(y$ein) #To make sure you are treating placeholder zeroes the same, make ein numeric for both!
x$ein <- as.numeric(x$ein)
y$ein <- as.numeric(y$ein)
sum(is.na(x$ein))
sum(is.na(y$ein)) #looks like the EINs are present for every single observation. 
ez1220_merged <- merge(x, y, by=c("ein","tax_pd"))
nrow(y) - # nrow(ez1220_merged)  #Why did so many rows get dropped?! That is not fantastic..could be the uneven coverage of the EO-BMF data. Need to look into this. It really could be the way that I make EINs numeric. I could be coercing some values to being different lengths than expected. Come back to this ***
write_csv(ez1220_merged, path="ez1220_merged.csv")


##Now doing the 990s from 2012 to 2020:
y <- read_csv("990s_1220_efficient.csv")
names(y)
typeof(x$tax_pd)
typeof(y$tax_pd)
typeof(x$ein)
typeof(y$ein) 
y$ein <- as.numeric(y$ein)
sum(is.na(y$ein))
reg_990s_1220_merged <- merge(x, y, by=c("ein","tax_pd"))
nrow(y) - nrow(reg_990s_1220_merged) #LOTS of rows getting dropped again. Need to figure this out.
write_csv(reg_990s_1220_merged, path="reg_990s_1220_merged.csv")
nrow(reg_990s_1220_merged)


###OKAY. THUS BEGINS THE INVESTIGATION INTO ALL OF THESE HORRIBLY MISSING ROWS. 
#How many rows in the original full_eobmf dataset don't have tax period information? That would be very bad too.
#Using a subsetted version of the EO-BMF (just Texas data) to see what might be going on. 
nrow(tx_eobmf[is.na(tx_eobmf$tax_year),]) / nrow(tx_eobmf) #23% of all values don't have tax period or year information. That is NOT good. It basically means that EO-BMF data is truly only good for assessing financial health of orgs and generally tying basic addresses to organizations generally. This may also very much explain why so many thousands of rows are getting dropped during merges of EO-BMF data and financial data!! 


#COME BACK TO THIS ***
#Now doing the 990s from 2013 to 2020, which contains thicker 990 details (because 2012 contained less info)
y <- read_csv("full_reg1320.csv")


######DATA EXPLORATION:
#Confirm: small organizations are also included in the EO-BMF? Ones that make like zero revenue?
names(full_eobmf)
nrow(full_eobmf [full_eobmf$income_amt<10,])
nrow(full_eobmf [is.na(full_eobmf$income_amt),])
#Yep, can confirm! That being said, quite a few organizations also don't have corresponding financial data in the EO-BMF, as an FYI.
