from Filter import Filter
from Algorithm import Algorithm
from Analysis import Analysis
from Aux import Aux

Aux = Aux()
DataFilter = Filter()
numOfFilesInRS = Aux.getNumOfFilesInResponseStack()

print('You got {0} datasets in your file'.format(DataFilter.countDatasets()))
print('The number of datasets in your ResponseStack is: {0}'.format(numOfFilesInRS))
dataRequired = input("Do you want new Data? y/n")

if dataRequired == 'y':

    numOfDs = input("How many datasets do you want?")

    print('getting data...')

    # extract relevant data

    data = DataFilter.cleanColumns(numOfDs)

    stop = True

    # Data filtering with diverse criteria

    cleanedData = DataFilter.filterCriteria(data)

    # write Data in CSV and print results grouped by category

    DataFilter.overViewCleanedData(cleanedData)

    # pass data to MS DL algorithm for analyzing the content of project pictures

    Algorithm = Algorithm()

    # get new Data from Microsoft and save response local

    Algorithm.getNewDataFromMS(cleanedData)

    # check Hypothesis from the local response stack

    numOfFilesInR = Aux.getNumOfFilesInStack()

    print('The process was successful, you got {0} new datasets'.format(numOfFilesInR))
    storeData = input('Do you want to store the new data in your stack? y/n')

    if storeData == 'y':
        Aux.storeResponseInStack()
    else:
        print('okay, nothing has been stored. Just watch you new Data')

print('alright, lets analyze the data from the stack')

responseStack = Aux.getDataFromResponseStack()

# group data by categories

Analysis = Analysis()

Analysis.buildCatsWithTargetVars(responseStack)

# build Statistics

Analysis.descriptiveStats(responseStack)

# make Regression

Analysis.makeRegression(responseStack)













