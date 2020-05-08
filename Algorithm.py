from Aux import Aux
import sys

import requests

# imports for computer-vision

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# imports for Text analysis

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')


class Algorithm():
    def __init__(self):
        self.VISION_KEY = 'd5fe8761733b42d0a44e3e327174c457'
        self.VISION_ENDPOINT = 'https://macomputervisionservice.cognitiveservices.azure.com/'
        self.TEXT_KEY = 'cd15a763eaf74a0d8d3744933a0d3e38'
        self.TEXT_ENDPOINT = 'https://matextanalyticsservice.cognitiveservices.azure.com/'

    Aux = Aux()

    def computerVision(self, cleanedData):

        computervision_client = ComputerVisionClient(self.VISION_ENDPOINT,
                                                     CognitiveServicesCredentials(self.VISION_KEY))
        # prepare picture data set

        remote_image_url = cleanedData[1]['algorithm']['photo']

        # get the image description in general

        description_results = computervision_client.describe_image(remote_image_url)

        if len(description_results.captions) > 0:

            tags = description_results.tags
            cleanedData[1]['results']['TagsInPic'] = tags
            cleanedData[1]['results']['NumOfObjectsInPic'] = len(tags)

            for caption in description_results.captions:
                confidence = caption.confidence * 100
                if confidence > 60:
                    cleanedData[1]['results']['hasContent'] = 'yes'
                    cleanedData[1]['results']['content'].append(caption.text)
                else:
                    cleanedData[1]['results']['hasContent'] = 'unsure'

            # get the picture category

            remote_image_features = ["categories"]
            categorize_results_remote = computervision_client.analyze_image(remote_image_url,
                                                                            remote_image_features)
            if len(categorize_results_remote.categories) > 0:
                for category in categorize_results_remote.categories:
                    if category.score * 100 > 60:
                        cleanedData[1]['results']['imageCategory'].append(category.name)
                    else:
                        cleanedData[1]['results']['imageCategory'].append('unsure')

            # get all objects in picture

            detect_objects_results_remote = computervision_client.detect_objects(remote_image_url)

            for objects in detect_objects_results_remote.objects:
                if objects.object == 'person' and objects.confidence * 100 > 60:
                    cleanedData[1]['results']['hasHuman'] = True

                    # check if a face of the person in visible

                    remote_image_features = ["faces"]
                    detect_faces_results_remote = computervision_client.analyze_image(remote_image_url,
                                                                                      remote_image_features)
                    if len(detect_faces_results_remote.faces) > 0:
                        cleanedData[1]['results']['hasFace'] = True

            # Color scheme

            remote_image_features = ["color"]
            detect_color_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
            picColor = detect_color_results_remote
            if not picColor.color.is_bw_img:
                cleanedData[1]['results']['hasColor'] = True
                background = picColor.color.dominant_color_background
                foreground = picColor.color.dominant_color_foreground
                colors = picColor.color.dominant_colors
                accentColor = picColor.color.accent_color

                if not background == 'Black' and not foreground == 'Black':
                    cleanedData[1]['results']['isBright'] = True
                if len(colors) > 2:
                    cleanedData[1]['results']['isColorful'] = True

                warmHue = self.Aux.getHue(accentColor)

                if warmHue:
                    cleanedData[1]['results']['hasWarmHue'] = True

        return cleanedData

    def getLengthSentiment(self, Text, client):

        response = client.analyze_sentiment(documents=Text)[0]
        sentimentTitle = response.sentiment
        sentiScoresTitle = [response.confidence_scores.positive, response.confidence_scores.neutral,
                            response.confidence_scores.negative]

        textLength = 0

        for idx, sentence in enumerate(response.sentences):
            textLength = textLength + sentence.grapheme_length

        result = [textLength, sentimentTitle, sentiScoresTitle]

        return result

    def getPhrases(self, Text, client):

        phrases = []

        try:
            response = client.extract_key_phrases(documents=Text)[0]

            if not response.is_error:
                for phrase in response.key_phrases:
                    phrases.append(phrase)
            else:
                phrases.append('Error')

        except Exception as err:
            print("Encountered exception. {}".format(err))

        return phrases

    def getOCRTags(self, picURL):

        picTags = []

        ocr_url = self.VISION_ENDPOINT + "vision/v2.1/ocr"
        headers = {'Ocp-Apim-Subscription-Key': self.VISION_KEY}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        data = {'url': picURL}
        response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()
        analysis = response.json()
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
        for word in word_infos:
            text = word["text"]
            picTags.append(text)

        return picTags

    def textAnalytics(self, VCleanData):

        ta_credential = AzureKeyCredential(self.TEXT_KEY)
        text_analytics_client = TextAnalyticsClient(endpoint=self.TEXT_ENDPOINT, credential=ta_credential)

        # analyze Title

        title = [VCleanData[1]['algorithm']['title']]

        # sentiment and length

        sentimentTitle = self.getLengthSentiment(title, text_analytics_client)

        VCleanData[1]['results']['lengthOfTitle'] = sentimentTitle[0]
        VCleanData[1]['results']['sentimentTitle'] = sentimentTitle[1]
        VCleanData[1]['results']['sentiScoresTitle'] = sentimentTitle[2]

        # get Key Phrases

        phrasesTitle = self.getPhrases(title, text_analytics_client)

        # -----------------------------

        # analyze Text

        text = [VCleanData[1]['algorithm']['text']]

        # sentiment and length

        sentimentText = self.getLengthSentiment(text, text_analytics_client)

        VCleanData[1]['results']['lengthOfTitle'] = sentimentText[0]
        VCleanData[1]['results']['sentimentText'] = sentimentText[1]
        VCleanData[1]['results']['sentiScoresText'] = sentimentText[2]

        # get Key Phrases

        phrasesText = self.getPhrases(title, text_analytics_client)

        # -----------------------------

        # analyze Title and Picture

        picTags = VCleanData[1]['results']['TagsInPic']
        phrases = phrasesTitle + phrasesText
        matchPic = self.Aux.textMatch(phrases, picTags)
        VCleanData[1]['results']['TextMatchPic'] = matchPic

        # analyze creator and title

        creator = [VCleanData[1]['algorithm']['creator']]
        matchCreator = self.Aux.textMatch(phrases, creator)
        VCleanData[1]['results']['TextMatchPic'] = matchCreator

        # analyze OCR in picture

        picUrl = {"url": VCleanData[1]['algorithm']['photo']}
        picTags = self.getOCRTags(picUrl)
