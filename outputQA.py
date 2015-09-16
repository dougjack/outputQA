# Attempt some basic QA of the CAPCOG output
# Doug Jackson
# doug.jackson@erg.com
from utilities.utilities import queryDB
import pandas as pd
import glob
import os
import numpy as np

##########################################################################################
# Constant definitions
##########################################################################################
workingDir = "C:/Users/SAC-DJackson/Documents/CAPCOG/outputQA"
transVMTfolder = "C:/Users/SAC-DJackson/Documents/CAPCOG/SEE_unzipped/TRANSVMT_2012_SCHOOL_WK"
hour = 20

countyID = 48021
numPollutantIDs = 25
numHours = 24
numFuelTypeIDs = 2
numSourceTypeIDs = 13

# Example data for one link and one hour from linksummarytotals
exampleLinkFile = "link3795.csv"

countyIDdatabase = "capcog_2012_summer_sa_14sep15_48453"

# Files and databases to QA offnet VMT
rampVMTfile = "C:/Users/SAC-DJackson/Documents/CAPCOG/outputQA/see_ramp_qa_capcog_2012_summer_sa_14sep15_48021.csv"
rampVMTdatabase = "capcog_2018_school_fr_09sep15b_offnet"

# Summary emissions database
defaultDB = "movesdb20141021cb6v2"
summaryDB = "capcog_2018_school_fr_09sep15b_summary"

##########################################################################################
# Run
##########################################################################################
os.chdir(workingDir)
#transVMTfile = glob.glob(os.path.join(transVMTfolder, "*.T" + "%02d" % hour))[0]
#
#data = pd.read_csv(transVMTfile, sep="\s+", header=False, 
#                   names=["Anode", "Bnode", "countyCode", "FuncClass",
#                          "Length", "Speed", "VMT", "Zone", "AreaTypeCode",
#                          "VCRatio"])
#
## Read the countyID to countyCode lookup table
#countyLookup = queryDB(countyIDdatabase, "SELECT * FROM countyLookup")
#
## Look up the countyCode
#countyCode = int(countyLookup.loc[countyLookup["countyID"]==countyID, "CountyCode"])
#
## Determine the number of links in this county
#valueCounts = data["countyCode"].value_counts()
#
#numLinks = valueCounts[countyCode]
#
#print("County", countyID, "has", numLinks, "links in file", transVMTfile)
#
## How many rows should there be in linksummarytotals?
#print("Total number of rows should be", numLinks*numPollutantIDs*numHours*numFuelTypeIDs*numSourceTypeIDs)
#print("Note: the actual number of rows in linksummarytotals won't match this because, e.g., some outputs are in *_offnet.idle_byzone.")
#
## Read in example results from linksummarytotals for one link
#exampleLink = pd.read_csv(exampleLinkFile, header=False, 
#                          names=["countyID", "linkID", "hourID", "Anode", "Bnode", "sourceTypeID",
#                                 "fuelTypeID", "roadTypeID", "pollutantID", "processID", "emissionsKG"])
#
#for index, row in exampleLink.iterrows():
#    exampleLink.loc[index, "pollutantProcessID"] = str(int(row["pollutantID"])) + "-" + str(int(row["processID"]))
#
## QA offnet VMT
#rampVMTtransvmt = pd.read_csv(rampVMTfile)                    
#crosstabVMTdaily = queryDB(rampVMTdatabase, "SELECT * FROM crosstabVMTdaily")           
#
## Sum the hourly VMT for just ramps
#rampVMTtransvmt = rampVMTtransvmt.loc[rampVMTtransvmt["roaddesc"]=="ramp"]  
#rampVMTtransvmtGrp = rampVMTtransvmt.groupby(["CountyID"], as_index=False)
#rampVMTtransvmtSum = rampVMTtransvmtGrp["VMT"].sum()     
#
## Calculate daily sum for each county from the crosstabbed VMT data
## First, stack the crosstabbed data
#VMTdaily = pd.melt(crosstabVMTdaily, id_vars=["countyID", "fuelTypeID", "roadtypeID"])   
#
## Sum the VMT by countyID
#VMTdailyGrp = VMTdaily.groupby(["countyID"], as_index=False)  
#VMTdailySum = VMTdailyGrp["value"].sum()  

# Confirm that the output has all of the pollutants that it should       
summaryTotals = queryDB(summaryDB, "SELECT * FROM summaryTotals")                        
pollutants = queryDB(defaultDB, "SELECT * FROM pollutant ORDER BY pollutantID")
pollutants.index = pollutants["pollutantID"]
summaryTotals["pollutantName"] = [pollutants.ix[int(row["pollutantID"]), "pollutantName"] for index, row in summaryTotals.iterrows()]
summaryTotals.to_csv("summaryTotals.csv", index=False)

# Confirm that the link-level output has all of the pollutants
linkSummaryTotals = queryDB(summaryDB, "SELECt * FROM linkSummaryTotals LIMIT 10000")

# Include only linkID 3838
linkSummaryTotals = linkSummaryTotals.loc[linkSummaryTotals["linkID"]==3838]
linkSummaryTotals["pollutantName"] = [pollutants.ix[int(row["pollutantID"]), "pollutantName"] for index, row in linkSummaryTotals.iterrows()]
linkSummaryTotals.to_csv("linkSummaryTotals.csv", index=False)