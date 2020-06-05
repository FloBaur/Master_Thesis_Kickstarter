from collections import Iterable
import os, os.path
import pickle
import shutil


class Aux():
    def __init__(self):
        self.DIR_RS = './Data/ResponseStack/'
        self.DIR_R = './Data/Response/'

    def getHue(self, color):

        isWarm = False

        aux = color.lstrip('#')
        rgbColor = tuple(int(aux[i:i + 2], 16) for i in (0, 2, 4))
        red = rgbColor[0]
        green = rgbColor[1]
        blue = rgbColor[2]

        minimum = min(min(red, green), blue)
        maximum = max(max(red, green), blue)

        if minimum == maximum:
            return 0

        if maximum == red:
            hue = (green - blue) / (maximum - minimum)

        elif maximum == green:
            hue = 2 + (blue - red) / (maximum - minimum)

        else:
            hue = 4 + (red - green) / (maximum - minimum)

        hue = hue * 60
        if hue < 0:
            hue = hue + 360

        roundedHue = round(hue)

        if 20 <= roundedHue <= 55 or 72 <= roundedHue <= 90 or 108 <= roundedHue <= 125 \
                or 143 <= roundedHue <= 162 or 180 <= roundedHue <= 198 or 234 <= roundedHue <= 253 or \
                270 <= roundedHue <= 289 or 270 <= roundedHue <= 289 or 306 <= roundedHue <= 325 or \
                342 <= roundedHue <= 360:
            isWarm = True

        answer = [isWarm, roundedHue]

        return answer

    def textMatch(self, phrases, tags):

        result = False

        match = {}

        if len(tags) > 0 and len(phrases) > 0:

            if bool(set(phrases).intersection(tags)):
                match = set(phrases).intersection(tags)
                result = True

        answer = [match, result]

        return answer

    def getCats(self, data):
        categories = []

        for row in data:
            categories.append(row['filter']['category'])

        setCat = set(categories)

        return setCat

    def flatten(self, lis):
        for item in lis:
            if isinstance(item, Iterable) and not isinstance(item, str):
                for x in self.flatten(item):
                    yield x
            else:
                yield item

        return lis

    def deleteDataFromFolder(self, DIR):

        stackFiles = os.listdir(DIR)

        for file in stackFiles:
            os.remove(os.path.join(DIR, file))

    def getDataFromResponseStack(self):

        responseStack = []

        for file in sorted(os.listdir(self.DIR_RS)):

            with open('{0}{1}'.format(self.DIR_RS, file), 'rb') as input:
                responseStack.append(pickle.load(input))

        return responseStack

    def getNumOfFilesInResponseStack(self):

        numOfFiles = len([name for name in os.listdir(self.DIR_RS) if os.path.isfile(os.path.join(self.DIR_RS, name))])

        return numOfFiles


    def getNumOfFilesInResponse(self):

        numOfFiles = len(os.listdir(self.DIR_R))
        return numOfFiles

    def storeResponseInStack(self):

        self.deleteDataFromFolder(self.DIR_RS)
        responseFiles = os.listdir(self.DIR_R)

        for file in responseFiles:
            shutil.move(self.DIR_R+file, self.DIR_RS)

    def storeDataInResponse(self, data):

        for row in data:
            with open('./Data/Response/%d.pkl' % row['key'], 'wb') as output:
                pickle.dump(row, output, pickle.HIGHEST_PROTOCOL)

    def stringifyText(self, text):
        try:
            stringifyText = str(text.text)
            if ',' in stringifyText:
                stringifyText = stringifyText.replace(',', '')
            if '.' in stringifyText:
                stringifyText = stringifyText.replace('.', '')
            num_Array = [int(s) for s in stringifyText.split() if s.isdigit()]
            if len(num_Array) > 0:
                number = num_Array[0]
            else:
                number = 0
        except Exception as E:
            number = 0
            print('Not possible to stringify Text ' + str(E))

        return number






