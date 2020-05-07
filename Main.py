from Filter import Filter
from Algorithm import Algorithm

# get raw Data from CSV File

DataFilter = Filter()

# extract relevant data

data = DataFilter.cleanColumns()

# Data filtering with diverse criteria

cleanedData = DataFilter.filterCriteria(data)

# write Data in CSV and print results grouped by category

DataFilter.overViewCleanedData(cleanedData)

Algorithm = Algorithm()

# pass data to MS DL algorithm for analyzing the content of project pictures

VCleanData = Algorithm.computerVision(cleanedData)  # UnitTest!!!

# pass data to MS DL algorithm for analyzing the content of project text

TVCleanData = Algorithm.textAnalytics(VCleanData)







