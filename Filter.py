import pandas as pd
import json
from datetime import datetime
from Aux import Aux
from Crawler import Crawler


class Filter():
    def __init__(self):
        self.data = pd.read_csv('./Data/Kickstarter.csv')

    Aux = Aux()
    Crawler = Crawler()


    def countDatasets(self):

        df = pd.DataFrame(self.data)
        numOfRows = len(df.index)

        return numOfRows

    def cleanColumns(self, numOfDs):

        global singleProject
        rightData = []

        counter = 0

        for pos, con in self.data.iterrows():
            if counter < int(numOfDs):
                try:
                    webUrl_JSON = json.loads(con['urls'])
                    webUrl = webUrl_JSON['web']['project']
                    rewUrl = webUrl_JSON['web']['rewards']

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
                            'backers': con['backers_count'],
                            'WebUrl': str(webUrl),
                            'RewUrl': str(rewUrl)
                        },
                        'algorithm': {
                            'photo': photo['1024x576'],
                            'title': con['slug'],
                            'text': con['blurb'],
                            'state': con['state'],
                            'creator': creator['name']
                        },
                        'colors': {
                            'background': '',
                            'foreground': '',
                            'dominantColors': [],
                            'accentColor': '',
                            'hue': 0
                        },
                        'results': {
                            'hasContent': 'no',  # computerVision  |
                            'content': [],  # computerVision  |
                            'imageCategory': [],  # computerVision  |
                            'hasHuman': 0,  # computerVision | Emo x
                            'hasFace': False,  # computerVision | Emo  -------> zweite Variante
                            'hasColor': False,  # computerVision | Emo
                            'isBright': True,  # computerVision | Emo
                            'hasManyDomColors': False,  # computerVision |
                            'hasWarmHueAccent': False,  # computerVision | Emo
                            'TagsInPic': [],  # computerVision |
                            'NumOfObjectsInPic': 0,  # computerVision |

                            'CLASS_fewObjects': False,   # INFO
                            'CLASS_normalObjects': False,  # INFO
                            'CLASS_manyObjects': False,

                            'lengthOfTitle': 0,  # textAnalytics |
                            'sentimentTitle': '',  # textAnalytics |
                            'sentiScoresTitle': [],  # textAnalytics |
                            'keyPhrasesTitle': [], # textAnalytics |
                            'lengthOfText': 0,  # textAnalytics |
                            'sentimentText': '',  # textAnalytics |
                            'sentiScoresText': [],  # textAnalytics |
                            'keyPhrasesText': [],  # textAnalytics |

                            'CLASS_shortTitle': False,   # INFO
                            'CLASS_normalTitle': False,  # INFO
                            'CLASS_longTitle': False,

                            'CLASS_negativeTitle': False,
                            'CLASS_neutralTitle': False,  # Emo # INFO
                            'CLASS_positiveTitle': False,  # Emo # INFO

                            'CLASS_shortText': False,  # INFO
                            'CLASS_normalText': False,   # INFO
                            'CLASS_longText': False,

                            'CLASS_negativeText': False,
                            'CLASS_neutralText': False,  # INFO
                            'CLASS_positiveText': False,  # Emo

                            'TextMatchPic': False,  # textAnalytics | TRUST -------> zweite Variante
                            'CreatorMatchTitle': False,  # textAnalytics | TRUST
                            'TitleMatchPicOCR': False,  # textAnalytics | TRUST
                            'OCRTags': False,
                            'OCRMatches': False,

                            'H1_Emotion': False,
                            'H2_ClearMassage': False,
                            'H3_Trust': False
                        }
                    }
                    rightData.append(singleProject)
                except:
                    continue

                counter = counter + 1


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

    def overViewCleanedData(self, data):

        global cat
        dataOverview = []
        catOverview = []

        for row in data:
            single = {
                'category': row['filter']['category'],
                'duration': row['filter']['duration'],
                'success': row['algorithm']['state'],
                'goal': row['filter']['goal'],
                'pledged': row['filter']['pledged'],
                'backers': row['filter']['backers'],
                '%pledged': round(row['filter']['pledged'] / row['filter']['goal'] * 100, 2)
            }
            dataOverview.append(single)

        cats = self.Aux.getCats(data)

        for rowCat in cats:
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
        df[column_order1].to_csv('./Data/FILTER_singleRow.csv')
        df2[column_order2].to_csv('./Data/FILTER_categoryAnalysis.csv')

    def getControllVars(self, data):

        data_Controls = []

        for row in data:

            webUrl = row['filter']['WebUrl']
            rewUrl = row['filter']['RewUrl']

            controls = self.Crawler.crawlData(webUrl, rewUrl)

            controls = {
                'controls': {
                    'numOfImg': controls[0],
                    'numOfRewards': controls[1],
                    'hasVideo': controls[2],
                    'texts': controls[3],
                    'text_Length': controls[4],
                    'hasFacebook': controls[5],
                    'numOfFbFriends': controls[6],
                    'experience': controls[7]
                }
            }

            updatedDict = {**row, **controls}
            data_Controls.append(updatedDict)

        return data_Controls
