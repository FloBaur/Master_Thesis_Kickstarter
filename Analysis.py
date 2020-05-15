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
                'TitleMatchPicOCR': row['results']['TitleMatchPicOCR'],
                'TextMatchPic': row['results']['TextMatchPic'],
                'CreatorMatchTitle': row['results']['CreatorMatchTitle'],
                'successful': row['algorithm']['state']
            }
            results.append(targetVars)

        return results

    def plotAndRegress(self, x, y):
        p1 = np.polyfit(x, y, 1)

        plt.plot(x, y, 'o')
        plt.plot(x, np.polyval(p1, x), 'r-')
        plt.show()

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        r_2 = pow(r_value, 2)

        return r_2, p_value

    def makeRegression(self, data):

        array = self.getTargetVariables(data)
        rawDf = pd.DataFrame(array)
        df = rawDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                            'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0})
        y = np.array(df['successful'].tolist())
        regResults = {}

        test2 = df.keys()

        x = np.array(df['hasContent'].tolist())
        regResults.update({'hasContent': self.plotAndRegress(x, y)})

        test3 = self.plotAndRegress(x, y)

        x = np.array(df['hasHuman'].tolist())
        regResults.update({'hasHuman': self.plotAndRegress(x, y)})

        x = np.array(df['hasFace'].tolist())
        regResults.update({'hasFace': self.plotAndRegress(x, y)})

        # x = np.array(df['hasColor'].tolist())
        # regResults.update({'hasColor': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['isBright'].tolist())
        # regResults.update({'isBright': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['hasManyDomColors'].tolist())
        # regResults.update({'hasManyDomColors': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['hasWarmHueAccent'].tolist())
        # regResults.update({'hasWarmHueAccent': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['NumOfObjectsInPic'].tolist())
        # regResults.update({'NumOfObjectsInPic': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['lengthOfTitle'].tolist())
        # regResults.update({'lengthOfTitle': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['lengthOfText'].tolist())
        # regResults.update({'lengthOfText': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['sentimentTitle'].tolist())
        # regResults.update({'sentimentTitle': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['sentimentText'].tolist())
        # regResults.update({'sentimentText': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['TitleMatchPicOCR'].tolist())
        # regResults.update({'TitleMatchPicOCR': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['TextMatchPic'].tolist())
        # regResults.update({'TextMatchPic': self.plotAndRegress(x, y)})
        #
        # x = np.array(df['CreatorMatchTitle'].tolist())
        # regResults.update({'CreatorMatchTitle': self.plotAndRegress(x, y)})

        stop = True

    def descriptiveStats(self, data):

        results = self.getTargetVariables(data)
        df = pd.DataFrame(results)

        column_order = ['category', 'hasContent', 'hasHuman', 'hasFace', 'hasColor', 'isBright', 'hasManyDomColors',
                        'hasWarmHueAccent', 'sentimentTitle', 'sentimentText', 'TitleMatchPicOCR', 'TextMatchPic',
                        'CreatorMatchTitle', 'NumOfObjectsInPic', 'lengthOfTitle', 'lengthOfText', 'successful']
        orderedDf = df[column_order]
        replacedDf = orderedDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                                        'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0})
        replacedDf[column_order].round(1).to_csv('./Data/singleRowResult.csv')
        descriptiveStatistic = replacedDf.describe()
        descriptiveStatistic.round(1).T.to_csv('./Data/descriptiveStatisticResults.csv')

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
                    if row['results']['sentimentTitle'] == 'positive':
                        sentimentTitlePos = sentimentTitlePos + 1
                    if row['results']['sentimentTitle'] == 'neutral':
                        sentimentTitleNeu = sentimentTitleNeu + 1
                    if row['results']['sentimentTitle'] == 'negative':
                        sentimentTitleNeg = sentimentTitleNeg + 1
                    if row['results']['sentimentText'] == 'positive':
                        sentimentTextPos = sentimentTextPos + 1
                    if row['results']['sentimentText'] == 'neutral':
                        sentimentTextNeu = sentimentTextNeu + 1
                    if row['results']['sentimentText'] == 'negative':
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
        df[column_order1].to_csv('./Data/categoryResult.csv')
