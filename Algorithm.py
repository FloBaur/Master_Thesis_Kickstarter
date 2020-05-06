from Aux import Aux
import sys

sys.path.append('/home/florian/anaconda3/lib/python3.7/site-packages')



# imports for computer-vision

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
from PIL import Image
import sys
import time


class Algorithm():
    def __init__(self):
        self.VISION_KEY = 'd5fe8761733b42d0a44e3e327174c457'
        self.VISION_ENDPOINT = 'https://macomputervisionservice.cognitiveservices.azure.com/'

    Aux = Aux()

    def computerVision(self, cleanedData):

        testColors = ['#BB6D10', '#C6A205']

        testHue = self.Aux.getHue(testColors)

        stop = True

        computervision_client = ComputerVisionClient(self.VISION_ENDPOINT,
                                                     CognitiveServicesCredentials(self.VISION_KEY))
        # collect picture data set

        remote_image_url = cleanedData[1]['algorithm']['photo']

        # get the image description in general
        # hier muss Schleife for picture in pictures rein

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
            print("Detecting objects in remote image:")
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
                numOfColors = len(colors)
                accentColor = picColor.color.accent_color
                colorsWithAccent = colors.append(accentColor)
                if not background == 'Black' and not foreground == 'Black':
                    cleanedData[1]['results']['isBright'] = True
                if numOfColors > 2:
                    cleanedData[1]['results']['isColorful'] = True

                warmHue = self.Aux.getHue(colorsWithAccent)

                if warmHue:
                    cleanedData[1]['results']['hasWarmHue'] = True

    def textAnalytics(self, data):
        print('Test')
