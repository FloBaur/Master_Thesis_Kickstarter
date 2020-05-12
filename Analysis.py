import pandas as pd
from Aux import Aux
import sys
import numpy as np
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy import stats
sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')


class Analysis():
    Aux = Aux()

    def getTargetVariables(self, data):

        results = []

        for row in data:
            targetVars = {
                'hasHuman': row['results']['hasHuman'],
                'hasFace': row['results']['hasFace'],
                'hasColor': row['results']['hasColor'],
                'isColorful': row['results']['isColorful'],
                'hasWarmHue': row['results']['hasWarmHue'],
                'isBright': row['results']['isBright'],
                'sentimentTitle': row['results']['sentimentTitle'],
                'sentimentText': row['results']['sentimentText'],
                'TitleMatchPicOCR': row['results']['TitleMatchPicOCR'],
                'TextMatchPic': row['results']['TextMatchPic'],
                'CreatorMatchTitle': row['results']['CreatorMatchTitle'],
                'successful': row['algorithm']['state']
            }
            results.append(targetVars)

        return results

    def makeRegression(self, AlgoData):

        targetVars = self.getTargetVariables(AlgoData)
        results = datasets.load_diabetes(targetVars)
        X = results.data
        y = results.target

        X2 = sm.add_constant(X)
        est = sm.OLS(y, X2)
        est2 = est.fit()
        print('Regression')
        print(est2.summary())

        lm = LinearRegression()
        lm.fit(X, y)
        params = np.append(lm.intercept_, lm.coef_)
        predictions = lm.predict(X)

        newX = pd.DataFrame({"Constant":np.ones(len(X))}).join(pd.DataFrame(X))
        MSE = (sum((y-predictions)**2))/(len(newX)-len(newX.columns))

        var_b = MSE*(np.linalg.inv(np.dot(newX.T,newX)).diagonal())
        sd_b = np.sqrt(var_b)
        ts_b = params / sd_b

        p_values = [2*(1-stats.t.cdf(np.abs(i), (len(newX)-1))) for i in ts_b]

        sd_b = np.round(sd_b, 3)
        ts_b = np.round(ts_b, 3)
        p_values = np.round(p_values, 3)
        params = np.round(params, 4)

        myDF3 = pd.DataFrame()
        myDF3["Coefficients"], myDF3["Standard Errors"], myDF3["t values"], myDF3["Probabilities"] = \
            [params, sd_b, ts_b, p_values]
        print(myDF3)

    def descriptiveStats(self, AlgoData):

        results = self.getTargetVariables(AlgoData)
        df = pd.DataFrame(results)
        df.describe()
        df.to_csv('./Data/Results4.csv')

    def buildCatsWithGoalVars(self, AlgoData):

        resultData = []

        cats = self.Aux.getCats(AlgoData)

        for rowCat in cats:
            proCounter = 0
            hasHuman = 0
            hasFace = 0
            hasColor = 0
            isBright = 0
            isColorful = 0
            hasWarmHue = 0
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

            for row in AlgoData:
                if row['results']['hasHuman']:
                    hasHuman = hasHuman + 1
                if row['results']['hasFace']:
                    hasFace = hasFace + 1
                if row['results']['hasColor']:
                    hasColor = hasColor + 1
                if row['results']['isBright']:
                    isBright = isBright + 1
                if row['results']['isColorful']:
                    isColorful = isColorful + 1
                if row['results']['hasWarmHue']:
                    hasWarmHue = hasWarmHue + 1
                if row['results']['sentimentTitle'] == 'positive':
                    sentimentTitlePos = sentimentTitlePos + 1
                if row['results']['sentimentTitle'] == 'neutral':
                    sentimentTitleNeu = sentimentTitleNeu + 1
                if row['results']['sentimentTitle'] == 'negative':
                    sentimentTitleNeg = sentimentTitleNeg + 1
                if row['results']['sentimentText'] == 'positive':
                    sentimentTextPos = sentimentTextPos + 1
                if row['results']['sentimentTitle'] == 'neutral':
                    sentimentTextNeu = sentimentTextNeu + 1
                if row['results']['sentimentTitle'] == 'negative':
                    sentimentTextNeg = sentimentTextNeg + 1
                if row['results']['TitleMatchPicOCR']:
                    TitleMatchPicOCR = TitleMatchPicOCR + 1
                if row['results']['TextMatchPic']:
                    TextMatchPic = TextMatchPic + 1
                if row['results']['CreatorMatchTitle']:
                    CreatorMatchTitle = CreatorMatchTitle + 1

                NumOfObjectsInPic = NumOfObjectsInPic + row['results']['NumOfObjectsInPic']
                lengthOfTitle = lengthOfTitle + row['results']['lengthOfTitle']
                lengthOfText = lengthOfText + row['results']['lengthOfText']
                proCounter = proCounter + 1

            catResult = {
                'Category': rowCat,
                'projects': proCounter,
                'persons': hasHuman,
                'faces': hasFace,
                'color': hasColor,
                'bright': isBright,
                'colorful': isColorful,
                'warm hue': hasWarmHue,
                'objects in pic AVG': round(NumOfObjectsInPic / proCounter),
                'positive Title': sentimentTitlePos,
                'neutral Title': sentimentTitleNeu,
                'negative Title': sentimentTitleNeg,
                'positive Text': sentimentTextPos,
                'neutral Text': sentimentTextNeu,
                'negative Text': sentimentTextNeg,
                'writing in pic match text': TitleMatchPicOCR,
                'text tags match pic Tags': TextMatchPic,
                'creator match title': CreatorMatchTitle,
                'length of title AVG': round(lengthOfTitle / proCounter),
                'length of text AVG': round(lengthOfText / proCounter)
            }

            resultData.append(catResult)

        df = pd.DataFrame(resultData)
        column_order1 = ['projects', 'persons', 'faces', 'color', 'bright', 'colorful', 'warm hue',
                         'objects in pic AVG', 'positive Title', 'neutral Title', 'negative Title', 'positive Text',
                         'neutral Text', 'negative Text', 'writing in pic match text', 'text tags match pic Tags',
                         'creator match title', 'length of title AVG', 'length of text AVG']
        df[column_order1].to_csv('./Data/Results3.csv')
