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

transVMTfolder = "C:/Users/SAC-DJackson/Documents/CAPCOG/SEE_unzipped/TRANSVMT_2012_SCHOOL_WK"
hour = 1

countyID = 48453

##########################################################################################
# Run
##########################################################################################
transVMTfile = glob.glob(os.path.join(transVMTfolder, "*.T" + "%02d" % hour))[0]

data = pd.read_csv(transVMTfile, sep="\s+", header=False, 
                   names=["Anode", "Bnode", "countyCode", "FuncClass",
                          "Length", "Speed", "VMT", "Zone", "AreaTypeCode",
                          "VCRatio"])

# Read the countyID to countyCode lookup table
countyLookup = queryDB("capcog_2018_school_fr_09sep15_48453", "SELECT * FROM countyLookup")

# Look up the countyCode
countyCode = int(countyLookup.loc[countyLookup["countyID"]==countyID, "CountyCode"])

# Determine the number of links in this county
valueCounts = data["countyCode"].value_counts()

print("County", countyID, "has", valueCounts[countyCode], "links in file", transVMTfile)