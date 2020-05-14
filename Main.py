from Filter import Filter
from Algorithm import Algorithm
from Analysis import Analysis

# get raw Data from CSV File

DataFilter = Filter()

# extract relevant data

data = DataFilter.cleanColumns()

# Data filtering with diverse criteria

cleanedData = DataFilter.filterCriteria(data)

# write Data in CSV and print results grouped by category

DataFilter.overViewCleanedData(cleanedData)

# pass data to MS DL algorithm for analyzing the content of project pictures

Algorithm = Algorithm()

VCleanData = Algorithm.computerVision(cleanedData)  # UnitTest!!! -> passed, check with DV

# pass data to MS DL algorithm for analyzing the content of project text

TVCleanData = Algorithm.textAnalytics(VCleanData)  # UnitTest!!! -> passed, check with DV

# group data by categories

Analysis = Analysis()

Analysis.buildCatsWithTargetVars(TVCleanData)

# build Statistics

Analysis.descriptiveStats(TVCleanData)  # UnitTest!!!

# make Regression

# Analysis.makeRegression(TVCleanData)  # UnitTest!!!













