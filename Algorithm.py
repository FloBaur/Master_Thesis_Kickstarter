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

    def computerVision(self, cleanedData):
        # examine data 'hasContent': None, 'content': 'no', 'hasHuman': 'no', 'hasFace': 'no',
        # 'ObjectsInPic': None, 'NumOfObjectsInPic': 0

        computervision_client = ComputerVisionClient(self.VISION_ENDPOINT,
                                                     CognitiveServicesCredentials(self.VISION_KEY))

        remote_image_url = cleanedData[1]['algorithm']['photo']

        # weg an Microsoft
        description_results = computervision_client.describe_image(remote_image_url)

        if len(description_results.captions) == 0:
            cleanedData[1]['results']['hasContent'] = 'no'
        #test

        else:
            tags = description_results.tags
            cleanedData[1]['results']['ObjectsInPic'] = tags
            cleanedData[1]['results']['NumOfObjectsInPic'] = len(tags)

            for caption in description_results.captions:
                confidence = caption.confidence * 100
                if confidence > 60:
                    cleanedData[1]['results']['hasContent'] = 'yes'
                    cleanedData[1]['results']['content'].append(caption.text)
                else:
                    cleanedData[1]['results']['hasContent'] = 'unsure'
        #test

        remote_image_features = ["categories"]
        categorize_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features) #ist da auch schon die discription drin
        if len(categorize_results_remote.categories) == 0:
            cleanedData[1]['results']['imageCategory'] = None
        else:
            for category in categorize_results_remote.categories:
                if category.score * 100 > 60:
                    cleanedData[1]['results']['imageCategory'].append(category.name)
                else:
                    cleanedData[1]['results']['imageCategory'].append('unsure')
        #test

        remote_image_features = ["faces"]
        detect_faces_results_remote = computervision_client.analyze_image(remote_image_url, remote_image_features)
        print("Faces in the remote image: ")
        if (len(detect_faces_results_remote.faces) == 0):
            print("No faces detected.")
        else:
            for face in detect_faces_results_remote.faces:
                print("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age,
                                                                         face.face_rectangle.left,
                                                                         face.face_rectangle.top,
                                                                         face.face_rectangle.left + face.face_rectangle.width,
                                                                         face.face_rectangle.top + face.face_rectangle.height))

    def analyzeFaces(self, data):
        print('Test')
