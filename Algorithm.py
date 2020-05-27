from Aux import Aux

import sys
sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# imports for Text analysis

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import requests
import re



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
        # # prepare picture data set
        for row in cleanedData:

            remote_image_url = row['algorithm']['photo']

            # get the image description in general

            description_results = computervision_client.describe_image(remote_image_url)

            if len(description_results.captions) > 0:

                tags = description_results.tags
                row['results']['TagsInPic'] = tags
                row['results']['NumOfObjectsInPic'] = len(tags)
                if len(tags) <= 5:
                    row['results']['CLASS_fewObjects'] = True
                elif len(tags) >= 20:
                    row['results']['CLASS_manyObjects'] = True
                else:
                    row['results']['CLASS_normalObjects'] = True

                for caption in description_results.captions:
                    confidence = caption.confidence * 100
                    if confidence > 50:
                        row['results']['hasContent'] = 'yes'
                        row['results']['content'].append(caption.text)
                    else:
                        row['results']['hasContent'] = 'unsure'
                        break

                # get the picture category

                remote_image_features = ["categories"]
                categorize_results_remote = computervision_client.analyze_image(remote_image_url,
                                                                                remote_image_features)
                if len(categorize_results_remote.categories) > 0:
                    for category in categorize_results_remote.categories:
                        if category.score * 100 > 50:
                            row['results']['imageCategory'].append(category.name)
                        else:
                            row['results']['imageCategory'].append('unsure')

                # get all objects in picture

                detect_objects_results_remote = computervision_client.detect_objects(remote_image_url)

                for objects in detect_objects_results_remote.objects:
                    if objects.object_property == 'person' and objects.confidence * 100 > 50:
                        row['results']['hasHuman'] = True

                        # check if a face of the person in visible

                        remote_image_features = ["faces"]
                        detect_faces_results_remote = computervision_client.analyze_image(remote_image_url,
                                                                                          remote_image_features)
                        if len(detect_faces_results_remote.faces) > 0:
                            row['results']['hasFace'] = True

                # Color scheme

                remote_image_features = ["color"]
                detect_color_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
                picColor = detect_color_results_remote
                if not picColor.color.is_bw_img:
                    row['results']['hasColor'] = True
                    background = picColor.color.dominant_color_background
                    row['colors']['background'] = background
                    foreground = picColor.color.dominant_color_foreground
                    row['colors']['foreground'] = foreground
                    dominantColors = picColor.color.dominant_colors
                    row['colors']['dominantColors'] = dominantColors
                    accentColor = picColor.color.accent_color
                    row['colors']['accentColor'] = accentColor

                    if background == 'Black' and foreground == 'Black':
                        row['results']['isBright'] = False
                    if len(dominantColors) > 2:
                        row['results']['hasManyDomColors'] = True

                    answer = self.Aux.getHue(accentColor)
                    hue = answer[1]
                    row['colors']['hue'] = hue
                    warmHue = answer[0]

                    if warmHue:
                        row['results']['hasWarmHueAccent'] = True

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
                    phrases.append(phrase.lower())
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
        test = str(picURL).replace("'", '"')
        data = {'url':  test}
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
            picTags.append(text.lower())

        return picTags

    def textAnalytics(self, VCleanData):

        ta_credential = AzureKeyCredential(self.TEXT_KEY)
        text_analytics_client = TextAnalyticsClient(endpoint=self.TEXT_ENDPOINT, credential=ta_credential)

        for row in VCleanData:
            title = [row['algorithm']['title']]

            # sentiment and length TITLE

            sentimentTitle = self.getLengthSentiment(title, text_analytics_client)

            row['results']['lengthOfTitle'] = sentimentTitle[0]

            if sentimentTitle[0] >= 47:
                row['results']['CLASS_longTitle'] = True
            elif sentimentTitle[0] <= 22:
                row['results']['CLASS_shortTitle'] = True
            else:
                row['results']['CLASS_normalTitle'] = True

            row['results']['sentimentTitle'] = sentimentTitle[1]
            if sentimentTitle[1] == 'positive':
                row['results']['CLASS_positiveTitle'] = True
            elif sentimentTitle[1] == 'neutral':
                row['results']['CLASS_neutralTitle'] = True
            else:
                row['results']['CLASS_negativeTitle'] = True

            row['results']['sentiScoresTitle'] = sentimentTitle[2]  # pos neu neg share

            # get Key Phrases in TITLE

            phrasesTitle = self.getPhrases(title, text_analytics_client)
            keyPhrasesTitle = []
            for phrase in phrasesTitle:
                phrase.replace('-', ' ')
                wordList = re.sub("[^\w]", " ",  phrase).split()
                keyPhrasesTitle.append(wordList)

            flattenedKeyPhrasesTitle = list(self.Aux.flatten(keyPhrasesTitle))
            row['results']['keyPhrasesTitle'] = flattenedKeyPhrasesTitle

            # analyze TEXT

            text = [row['algorithm']['text']]

            # sentiment and length TEXT

            sentimentText = self.getLengthSentiment(text, text_analytics_client)

            row['results']['lengthOfText'] = sentimentText[0]
            if sentimentText[0] >= 131:
                row['results']['CLASS_longText'] = True
            elif sentimentText[0] <= 100:
                row['results']['CLASS_shortText'] = True
            else:
                row['results']['CLASS_normalText'] = True

            row['results']['sentimentText'] = sentimentText[1]
            if sentimentText[1] == 'positive':
                row['results']['CLASS_positiveText'] = True
            elif sentimentText[1] == 'neutral':
                row['results']['CLASS_neutralText'] = True
            else:
                row['results']['CLASS_negativeText'] = True

            row['results']['sentiScoresText'] = sentimentText[2]

            # get Key Phrases TEXT

            phrasesText = self.getPhrases(text, text_analytics_client)
            keyPhrasesText = []
            for phrase in phrasesText:
                phrase.replace('-', ' ')
                wordList = re.sub("[^\w]", " ",  phrase).split()
                keyPhrasesText.append(wordList)

            flattenedKeyPhrasesText = list(self.Aux.flatten(keyPhrasesText))

            row['results']['keyPhrasesText'] = flattenedKeyPhrasesText

            # analyze TITLE TEXT and Picture

            picTags = row['results']['TagsInPic']
            phrases = flattenedKeyPhrasesText + flattenedKeyPhrasesTitle
            matchPic = self.Aux.textMatch(phrases, picTags)
            row['results']['TextMatchPic'] = matchPic[1]

            # analyze creator and TITLE TEXT

            creator = row['algorithm']['creator']
            matchCreator = self.Aux.textMatch(phrases, creator)
            row['results']['CreatorMatchTitle'] = matchCreator[1]

            # analyze OCR in picture

            picUrl = row['algorithm']['photo'].lstrip("'")
            OCRTags = self.getOCRTags(picUrl)
            if len(OCRTags) > 0:
                row['results']['OCRTags'] = OCRTags

            TextMatchOCR = self.Aux.textMatch(phrases, OCRTags)
            row['results']['OCRMatches'] = TextMatchOCR[0]
            row['results']['TitleMatchPicOCR'] = TextMatchOCR[1]

        return VCleanData


