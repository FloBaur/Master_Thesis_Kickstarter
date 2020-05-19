import pandas as pd
from Aux import Aux
import matplotlib.pyplot as plt
from scipy.stats import *
import numpy as np


class Analysis():
    Aux = Aux()

    def getTargetVariables(self, data):

        results = []

        for row in data:
            targetVars = {
                'category': row['filter']['category'],
                'hasContent': row['results']['hasContent'],
                'hasHuman': row['results']['hasHuman'],
                'hasFace': row['results']['hasFace'],
                'hasColor': row['results']['hasColor'],
                'isBright': row['results']['isBright'],
                'hasManyDomColors': row['results']['hasManyDomColors'],
                'hasWarmHueAccent': row['results']['hasWarmHueAccent'],
                'NumOfObjectsInPic': row['results']['NumOfObjectsInPic'],
                'lengthOfTitle': row['results']['lengthOfTitle'],
                'lengthOfText': row['results']['lengthOfText'],
                'sentimentTitle': row['results']['sentimentTitle'],
                'sentimentText': row['results']['sentimentText'],
                'TitleMatchPicOCR': row['results']['TitleMatchPicOCR'],  # doesn't work because of Api regulation
                'TextMatchPic': row['results']['TextMatchPic'],
                'CreatorMatchTitle': row['results']['CreatorMatchTitle'],

                'CLASS_fewObjects': row['results']['CLASS_fewObjects'],
                'CLASS_normalObjects': row['results']['CLASS_normalObjects'],
                'CLASS_manyObjects': row['results']['CLASS_manyObjects'],

                'CLASS_shortTitle': row['results']['CLASS_shortTitle'],
                'CLASS_normalTitle': row['results']['CLASS_normalTitle'],
                'CLASS_longTitle': row['results']['CLASS_longTitle'],

                'CLASS_negativeTitle': row['results']['CLASS_negativeTitle'],
                'CLASS_neutralTitle': row['results']['CLASS_neutralTitle'],
                'CLASS_positiveTitle': row['results']['CLASS_positiveTitle'],

                'CLASS_shortText': row['results']['CLASS_shortText'],
                'CLASS_normalText': row['results']['CLASS_normalText'],
                'CLASS_longText': row['results']['CLASS_longText'],

                'CLASS_negativeText': row['results']['CLASS_negativeText'],
                'CLASS_neutralText': row['results']['CLASS_neutralText'],
                'CLASS_positiveText': row['results']['CLASS_positiveText'],

                'successful': row['algorithm']['state']
            }
            results.append(targetVars)

        return results

    def plotAndRegress(self, x, y):

        isSignificant = False
        p1 = np.polyfit(x, y, 1)

        plt.plot(x, y, 'o')
        plt.plot(x, np.polyval(p1, x), 'r-')
        plt.show()

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        r_2 = pow(r_value, 2)

        if p_value < 0.1:
            isSignificant = True

        return r_2, p_value, isSignificant

    def makeRegression(self, data):

        array = self.getTargetVariables(data)

        rawDf = pd.DataFrame(array)
        df = rawDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                            'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0, 'mixed': 0.5})
        y = np.array(df['successful'])
        regResults = {}

        CATS = ['hasHuman', 'hasFace', 'hasColor', 'isBright', 'hasManyDomColors', 'hasWarmHueAccent', 'TextMatchPic',
                'CreatorMatchTitle',  # OCR Variable missing
                'CLASS_manyObjects', 'CLASS_normalObjects', 'CLASS_fewObjects',
                'CLASS_positiveTitle', 'CLASS_neutralTitle', 'CLASS_negativeTitle',
                'CLASS_longTitle', 'CLASS_normalTitle', 'CLASS_shortTitle',
                'CLASS_longText', 'CLASS_normalText', 'CLASS_shortText',
                'CLASS_positiveText', 'CLASS_neutralText', 'CLASS_negativeText']

        stop = True

        for key in CATS:

            x = np.array(df[key])
            answer = self.plotAndRegress(x, y)
            regResults.update({key: {
                'r2': answer[0],
                'significance': answer[1],
                'is_Significant': answer[2]
            }})

    def descriptiveStats(self, data):

        results = self.getTargetVariables(data)
        df = pd.DataFrame(results)

        column_order = ['category', 'hasContent', 'hasHuman', 'hasFace', 'hasColor', 'isBright', 'hasManyDomColors',
                        'hasWarmHueAccent', 'sentimentTitle', 'sentimentText', 'TitleMatchPicOCR', 'TextMatchPic',
                        'CreatorMatchTitle', 'NumOfObjectsInPic', 'lengthOfTitle', 'lengthOfText', 'successful']
        orderedDf = df[column_order]
        replacedDf = orderedDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                                        'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0,
                                        'mixed': 0.5})
        replacedDf[column_order].round(1).to_csv('./Data/ANALYSIS_singleRow.csv')
        descriptiveStatistic = replacedDf.describe()
        descriptiveStatistic.round(1).T.to_csv('./Data/ANALYSIS_DescriptiveStatistics.csv')

    def buildCatsWithTargetVars(self, data):

        resultData = []

        cats = self.Aux.getCats(data)

        for rowCat in cats:
            proCounter = 0
            hasContent = 0
            hasHuman = 0
            hasFace = 0
            hasColor = 0
            isBright = 0
            hasManyDomColors = 0
            hasWarmHueAccent = 0
            NumOfObjectsInPic = 0  # sum
            lengthOfTitle = 0  # sum
            sentimentTitlePos = 0
            sentimentTitleNeu = 0
            sentimentTitleNeg = 0
            sentimentTextPos = 0
            sentimentTextNeu = 0
            sentimentTextNeg = 0
            lengthOfText = 0  # sum
            TitleMatchPicOCR = 0
            TextMatchPic = 0
            CreatorMatchTitle = 0

            for row in data:
                if row['filter']['category'] == rowCat:
                    proCounter = proCounter + 1
                    NumOfObjectsInPic = NumOfObjectsInPic + row['results']['NumOfObjectsInPic']
                    lengthOfTitle = lengthOfTitle + row['results']['lengthOfTitle']
                    lengthOfText = lengthOfText + row['results']['lengthOfText']
                    if row['results']['hasContent'] == 'yes':
                        hasContent = hasContent + 1
                    if row['results']['hasHuman']:
                        hasHuman = hasHuman + 1
                    if row['results']['hasFace']:
                        hasFace = hasFace + 1
                    if row['results']['hasColor']:
                        hasColor = hasColor + 1
                    if row['results']['isBright']:
                        isBright = isBright + 1
                    if row['results']['hasManyDomColors']:
                        hasManyDomColors = hasManyDomColors + 1
                    if row['results']['hasWarmHueAccent']:
                        hasWarmHueAccent = hasWarmHueAccent + 1
                    if row['results']['CLASS_positiveTitle']:
                        sentimentTitlePos = sentimentTitlePos + 1
                    if row['results']['CLASS_neutralTitle']:
                        sentimentTitleNeu = sentimentTitleNeu + 1
                    if row['results']['CLASS_negativeTitle']:
                        sentimentTitleNeg = sentimentTitleNeg + 1
                    if row['results']['CLASS_positiveText']:
                        sentimentTextPos = sentimentTextPos + 1
                    if row['results']['CLASS_neutralText']:
                        sentimentTextNeu = sentimentTextNeu + 1
                    if row['results']['CLASS_negativeText']:
                        sentimentTextNeg = sentimentTextNeg + 1
                    if row['results']['TitleMatchPicOCR']:
                        TitleMatchPicOCR = TitleMatchPicOCR + 1
                    if row['results']['TextMatchPic']:
                        TextMatchPic = TextMatchPic + 1
                    if row['results']['CreatorMatchTitle']:
                        CreatorMatchTitle = CreatorMatchTitle + 1

            catResult = {
                'category': rowCat,
                'projects': proCounter,
                'persons': round(hasHuman / proCounter * 100),
                'faces': round(hasFace / proCounter * 100),
                'color': round(hasColor / proCounter * 100),
                'bright': round(isBright / proCounter * 100),
                'many dominant colors': round(hasManyDomColors / proCounter * 100),
                'warm hue accent': round(hasWarmHueAccent / proCounter * 100),
                'positive title': round(sentimentTitlePos / proCounter * 100),
                'neutral title': round(sentimentTitleNeu / proCounter * 100),
                'negative title': round(sentimentTitleNeg / proCounter * 100),
                'positive text': round(sentimentTextPos / proCounter * 100),
                'neutral text': round(sentimentTextNeu / proCounter * 100),
                'negative text': round(sentimentTextNeg / proCounter * 100),
                'OCR match text': round(TitleMatchPicOCR / proCounter * 100),
                'text match pic tags': round(TextMatchPic / proCounter * 100),
                'creator match title': round(CreatorMatchTitle / proCounter * 100),
                'objects in pic AVG': round(NumOfObjectsInPic / proCounter),
                'length of title AVG': round(lengthOfTitle / proCounter),
                'length of text AVG': round(lengthOfText / proCounter)
            }

            resultData.append(catResult)

        df = pd.DataFrame(resultData)
        column_order1 = ['category', 'projects', 'persons', 'faces', 'color', 'bright', 'many dominant colors',
                         'warm hue accent', 'positive title', 'neutral title', 'negative title',
                         'positive text', 'neutral text', 'negative text', 'OCR match text',
                         'text match pic tags', 'creator match title', 'objects in pic AVG', 'length of title AVG',
                         'length of text AVG']
        df[column_order1].to_csv('./Data/ANALYSIS_CategoryResult.csv')
