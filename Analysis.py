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
            targetVars = row['results']
            controlVars = row['controls']
            extraVars = {
                'successful': row['algorithm']['state'],
                'category': row['filter']['category'],
                'CON_goal': row['filter']['goal'],
                'CON_duration': row['filter']['duration']
            }

            TCE_Dict = {**targetVars, **controlVars, **extraVars}
            results.append(TCE_Dict)

        return results

    def plotAndRegress(self, x, y):

        isSignificant = False
        p1 = np.polyfit(x, y, 1)

        plt.plot(x, y, 'o')
        plt.plot(x, np.polyval(p1, x), 'r-')
        plt.show()

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        r_2 = pow(r_value, 2)

        if p_value < 0.05:
            isSignificant = True

        return r_2, p_value, isSignificant, slope

    def makeRegression(self, data):

        array = self.getTargetVariables(data)

        rawDf = pd.DataFrame(array)
        df = rawDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                            'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0, 'mixed': 0.5})
        y = np.array(df['successful'])
        regResults = {}

        CATS = ['hasHuman', 'hasFace', 'hasColor', 'isBright', 'hasManyDomColors', 'hasWarmHueAccent',
                'TextMatchPic', 'CreatorMatchTitle', 'TitleMatchPicOCR',
                'CLASS_manyObjects', 'CLASS_normalObjects', 'CLASS_fewObjects',
                'CLASS_positiveTitle', 'CLASS_neutralTitle', 'CLASS_negativeTitle',
                'CLASS_longTitle', 'CLASS_normalTitle', 'CLASS_shortTitle',
                'CLASS_longText', 'CLASS_normalText', 'CLASS_shortText',
                'CLASS_positiveText', 'CLASS_neutralText', 'CLASS_negativeText',
                'H1_Emotion', 'H2_ClearMassage', 'H3_Trust',
                'CON_numOfImg', 'CON_numOfRewards', 'CON_hasVideo', 'CON_text_Length', 'CON_numOfFbFriends',
                'CON_experience', 'CON_goal', 'CON_duration'
                ]

        for key in CATS:

            x = df[key]
            validCheckSum = 0
            coefficient = '-'
            for val in x:
                validCheckSum = validCheckSum + val
            if validCheckSum != 0:

                X = np.array(x)
                answer = self.plotAndRegress(X, y)
                if answer[3] > 0:
                    coefficient = '+'

                regResults.update({key: {
                    'r2': answer[0],
                    'significance': answer[1],
                    'is_Significant': answer[2],
                    'coefficient': coefficient
                }})

        dfResult = pd.DataFrame(regResults)
        dfResult.round(2).T.to_csv('./Data/Results/ANALYSIS_RegressionResult.csv')

    def descriptiveStats(self, data):

        results = self.getTargetVariables(data)
        df = pd.DataFrame(results)

        column_order = ['category', 'hasContent', 'hasHuman', 'hasFace', 'hasColor', 'isBright', 'hasManyDomColors',
                        'hasWarmHueAccent', 'sentimentTitle', 'sentimentText', 'TitleMatchPicOCR', 'TextMatchPic',
                        'CreatorMatchTitle', 'NumOfObjectsInPic', 'lengthOfTitle', 'lengthOfText',
                        'H1_Emotion', 'H2_ClearMassage', 'H3_Trust',
                        'CON_numOfImg', 'CON_numOfRewards', 'CON_hasVideo', 'CON_text_Length', 'CON_numOfFbFriends',
                        'CON_experience', 'CON_goal', 'CON_duration',
                        'successful']
        orderedDf = df[column_order]
        replacedDf = orderedDf.replace({'unsure': 0, 'positive': 1, 'negative': 0, 'neutral': 0.5,
                                        'successful': 1, 'failed': 0, 'yes': 1, 'no': 0, True: 1, False: 0,
                                        'mixed': 0.5})
        replacedDf[column_order].round(1).to_csv('./Data/Results/ANALYSIS_singleRow.csv')
        descriptiveStatistic = replacedDf.describe()
        descriptiveStatistic.round(1).T.to_csv('./Data/Results/ANALYSIS_DescriptiveStatistics.csv')

    def buildCatsWithTargetVars(self, data):

        resultData = []
        cats = self.Aux.getCats(data)

        for rowCat in cats:
            proCounter, hasContent, hasHuman, hasFace, hasColor, isBright, hasManyDomColors, hasWarmHueAccent, \
                NumOfObjectsInPic, lengthOfTitle, sentimentTitlePos, sentimentTitleNeu, sentimentTitleNeg, \
                sentimentTextPos, sentimentTextNeu, sentimentTextNeg, lengthOfText, TitleMatchPicOCR, TextMatchPic, \
                CreatorMatchTitle, H1_Emotion, H2_ClearMassage, H3_Trust, \
                CON_numOfImg, CON_numOfRewards, CON_hasVideo, CON_text_Length, CON_numOfFbFriends, CON_experience \
                = (0,) * 29

            for row in data:
                if row['filter']['category'] == rowCat:

                    proCounter = proCounter + 1
                    NumOfObjectsInPic = NumOfObjectsInPic + row['results']['NumOfObjectsInPic']
                    lengthOfTitle = lengthOfTitle + row['results']['lengthOfTitle']
                    lengthOfText = lengthOfText + row['results']['lengthOfText']
                    CON_numOfImg = CON_numOfImg + row['controls']['CON_numOfImg']
                    CON_numOfRewards = CON_numOfRewards + row['controls']['CON_numOfRewards']
                    CON_text_Length = CON_text_Length + row['controls']['CON_text_Length']
                    CON_numOfFbFriends = CON_numOfFbFriends + row['controls']['CON_numOfFbFriends']
                    CON_experience = CON_experience + row['controls']['CON_experience']

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
                    if row['results']['H1_Emotion']:
                        H1_Emotion = H1_Emotion + 1
                    if row['results']['H2_ClearMassage']:
                        H2_ClearMassage = H2_ClearMassage + 1
                    if row['results']['H3_Trust']:
                        H3_Trust = H3_Trust + 1
                    if row['controls']['CON_hasVideo']:
                        CON_hasVideo = CON_hasVideo + 1

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
                'length of text AVG': round(lengthOfText / proCounter),
                'H1_Emotion': round(H1_Emotion / proCounter * 100),
                'H2_ClearMassage': round(H2_ClearMassage / proCounter * 100),
                'H3_Trust': round(H3_Trust / proCounter * 100),
                'CON_numOfImg': round(CON_numOfImg / proCounter),
                'CON_numOfRewards': round(CON_numOfRewards / proCounter),
                'CON_hasVideo': round(CON_hasVideo / proCounter * 100),
                'CON_text_Length': round(CON_text_Length / proCounter),
                'CON_numOfFbFriends': round(CON_numOfFbFriends / proCounter),
                'CON_experience': round(CON_experience / proCounter)
            }

            resultData.append(catResult)

        df = pd.DataFrame(resultData)
        column_order1 = ['category', 'projects', 'persons', 'faces', 'color', 'bright', 'many dominant colors',
                         'warm hue accent', 'positive title', 'neutral title', 'negative title',
                         'positive text', 'neutral text', 'negative text', 'OCR match text',
                         'text match pic tags', 'creator match title', 'objects in pic AVG', 'length of title AVG',
                         'length of text AVG', 'H1_Emotion', 'H2_ClearMassage', 'H3_Trust',
                         'CON_numOfImg', 'CON_numOfRewards', 'CON_hasVideo', 'CON_text_Length', 'CON_numOfFbFriends',
                         'CON_experience']
        df[column_order1].to_csv('./Data/Results/ANALYSIS_CategoryResult.csv')
