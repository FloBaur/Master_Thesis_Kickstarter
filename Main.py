from Filter import Filter
from Algorithm import Algorithm
from Analysis import Analysis
from Aux import Aux

Aux = Aux()
DataFilter = Filter()
Analysis = Analysis()
numOfFilesInRS = Aux.getNumOfFilesInResponseStack()

print('You got {0} datasets in your file'.format(DataFilter.countDatasets()))
print('The number of datasets in your ResponseStack is: {0}'.format(numOfFilesInRS))
print("Do you want new Data? y/n")
dataRequired = input()

if dataRequired == 'y':

    try:
        print("How many datasets do you want?")
        numOfDs = input()

        print('getting data from crawler...')

        # extract relevant data

        data = DataFilter.cleanColumns(numOfDs)

        # Data filtering with diverse criteria

        cleanedData = DataFilter.filterCriteria(data)

        # get control variables by crawler

        cleanedData_Control = DataFilter.getControllVars(cleanedData)

        # write Data in CSV and print results grouped by category

        DataFilter.overViewCleanedData(cleanedData_Control)

        # pass data to MS DL algorithm for analyzing the content of project pictures

        Algorithm = Algorithm()

        # get new Data from Microsoft and save response local

        print('getting data from Microsoft...')

        Algorithm.getNewDataFromMS(cleanedData_Control)

        numOfFilesInR = Aux.getNumOfFilesInStack()

        print('The process was successful, you got {0} new datasets'.format(numOfFilesInR))
        print('Do you want to store the new data in your stack? y/n')
        storeData = input()

        if storeData == 'y':
            Aux.storeResponseInStack()
        else:
            print('okay, nothing has been stored. Just watch you new Data')
    except NameError:
        print("An Error occurred")

print('alright, lets analyze the data from the stack')

responseStack_Unsorted = Aux.getDataFromResponseStack()

# group data by categories

responseStack = sorted(responseStack_Unsorted, key=lambda k: k['key'])

Analysis.buildCatsWithTargetVars(responseStack)

# build Statistics

Analysis.descriptiveStats(responseStack)

while True:

    print('What should be your TARGET_VAR for regression?')
    print('Success = s')
    print('Pledged money = p')
    print('Number of backers = b')
    TARGET_VAR = input()

    # Regression analysis

    if TARGET_VAR in ('s', 'p', 'b'):
        answer = True
        Analysis.makeRegression(responseStack, TARGET_VAR)
        break

    else:
        print('your input was not correct')
        print()

print('Your analysis was successful')




















