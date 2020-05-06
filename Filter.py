import pandas as pd
import json
from datetime import datetime


class Filter():
    def __init__(self):
        self.data = pd.read_csv('./Data/Kickstarter.csv')

    def cleanColumns(self):
        global singleProject
        rightData = []

        counter = 0

        for pos, con in self.data.iterrows():
            if counter < 4000:
                try:
                    category = json.loads(con['category'])
                    creator = json.loads(con['creator'])
                    photo = json.loads(con['photo'])
                    duration = datetime.fromtimestamp(con['state_changed_at']) - datetime.fromtimestamp(
                        con['launched_at'])

                    singleProject = {
                        'key': counter,
                        'id': con['id'],
                        'filter': {
                            'category': category['parent_name'],
                            'country': con['country'],
                            'currency': con['currency'],
                            'goal': con['goal'],
                            'duration': duration.days,
                            'pledged': con['pledged'],
                            'backers': con['backers_count']
                        },
                        'algorithm': {
                            'photo': photo['ed'],
                            'title': con['slug'],
                            'text': con['blurb'],
                            'state': con['state'],
                            'creator': creator['name']
                        },
                        'results': {
                            'hasContent': 'no', # computerVision  |
                            'content': [], # computerVision  |
                            'imageCategory': [], # computerVision  |
                            'hasHuman': False, # computerVision |
                            'hasFace': False, # computerVision |
                            'hasColor': False,   # computerVision |
                            'isBright': False,   # computerVision
                            'TagsInPic': [], # computerVision  |
                            'NumOfObjectsInPic': 0, # computerVision  |
                            'lengthOfText': 0,
                            'TitleMatchPicOCR': 'no',
                            'TextMatchPic': 'no',
                            'CreatorMatchTitle': 'no',
                        }
                    }
                except:
                    continue

                counter = counter + 1
                rightData.append(singleProject)

        return rightData

    def filterCriteria(self, data):

        cleanedArray = []

        for row in data:
            if row['filter']['country'] == 'US' and row['filter']['currency'] == 'USD' and \
                    100 <= row['filter']['goal'] <= 1000000 and row['algorithm']['state'] != 'canceled' and \
                    row['algorithm']['state'] != 'live' and row['algorithm']['state'] != 'suspended' and \
                    row['filter']['duration'] <= 60:
                cleanedArray.append(row)

        for row in cleanedArray:
            row['key'] = cleanedArray.index(row)

        return cleanedArray

    def overViewCleanedData(self, cleanedData):

        global cat
        dataOverview = []
        categories = []
        catOverview = []

        for row in cleanedData:
            singleCleaned = {
                'category': row['filter']['category'],
                'duration': row['filter']['duration'],
                'success': row['algorithm']['state'],
                'goal': row['filter']['goal'],
                'pledged': row['filter']['pledged'],
                'backers': row['filter']['backers'],
                '%pledged': round(row['filter']['pledged'] / row['filter']['goal'] * 100, 2)
            }
            dataOverview.append(singleCleaned)

        for row in dataOverview:
            categories.append(row['category'])

        setCat = set(categories)

        for rowCat in setCat:
            GoalSum = 0
            ProjectCounter = 0
            SuccessCounter = 0
            FundingRatio = 0
            BackersSum = 0
            Duration = 0
            for row in dataOverview:
                if row['category'] == rowCat:
                    ProjectCounter = ProjectCounter + 1
                    GoalSum = GoalSum + row['goal']
                    FundingRatio = FundingRatio + row['%pledged']
                    BackersSum = BackersSum + row['backers']
                    Duration = Duration + row['duration']
                    if row['success'] == 'successful':
                        SuccessCounter = SuccessCounter + 1

            cat = {
                'Category': rowCat,
                'Project counter': ProjectCounter,
                'Successful projects': SuccessCounter,
                'Success rate AVG[%]': round(SuccessCounter / ProjectCounter * 100, 2),
                'Goal AVG[$]': round(GoalSum / ProjectCounter),
                'Funding ratio AVG[%]': round(FundingRatio / ProjectCounter, 2),
                'Backers AVG': round(BackersSum / ProjectCounter),
                'Duration AVG[days]': round(Duration / ProjectCounter, 1)

            }

            catOverview.append(cat)

        df = pd.DataFrame(dataOverview)
        df2 = pd.DataFrame(catOverview)
        column_order1 = ['category', 'duration', 'success', 'goal', 'pledged', 'backers', '%pledged']
        column_order2 = ['Category', 'Project counter', 'Successful projects', 'Success rate AVG[%]', 'Goal AVG[$]',
                         'Funding ratio AVG[%]', 'Backers AVG', 'Duration AVG[days]']
        df[column_order1].to_csv('./Data/Results.csv')
        df2[column_order2].to_csv('./Data/Results2.csv')
