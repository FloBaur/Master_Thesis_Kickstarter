from Filter import Filter
from Algorithm import Algorithm
from Analysis import Analysis
from Aux import Aux

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

VCleanData = Algorithm.computerVision(cleanedData)

# pass data to MS DL algorithm for analyzing the content of project text

TVCleanData = Algorithm.textAnalytics(VCleanData)

# check Hypothesis

Aux = Aux()

readyData = Aux.checkHypothesis(TVCleanData)

# group data by categories

Analysis = Analysis()

Analysis.buildCatsWithTargetVars(readyData)

# build Statistics

Analysis.descriptiveStats(readyData)

# make Regression

Analysis.makeRegression(readyData)













