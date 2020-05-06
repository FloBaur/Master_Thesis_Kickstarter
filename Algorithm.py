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
        test = None
        description_results = computervision_client.describe_image(remote_image_url)

        if len(description_results.captions) == 0:
            cleanedData[1]['results']['hasContent'] = 'no'

        else:
            tags = description_results.tags
            numOfTags = len(tags)
            cleanedData[1]['results']['ObjectsInPic'] = tags
            cleanedData[1]['results']['NumOfObjectsInPic'] = numOfTags

            # hier muss noch was gemacht werden

            for caption in description_results.captions:
                text = caption.text
                confidence = caption.confidence * 100
                cleanedData[1]['results']['hasContent'] = 'yes'
                cleanedData[1]['results']['content'] = text

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
