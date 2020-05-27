from collections import Iterable


class Aux():

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

    def checkHypothesis(self, data):

        for row in data:

            if row['results']['hasHuman'] and row['results']['hasColor'] and row['results']['isBright'] and \
                    not row['results']['CLASS_negativeTitle'] and \
                    row['results']['CLASS_positiveText'] and row['results']['hasWarmHueAccent']:

                row['results']['H1_Emotion'] = True

            if not row['results']['CLASS_manyObjects'] and not row['results']['CLASS_longTitle'] and \
                    not row['results']['CLASS_longText'] and \
                    row['results']['CLASS_neutralText'] and not row['results']['CLASS_negativeTitle']:

                row['results']['H2_ClearMassage'] = True

            if row['results']['CreatorMatchTitle'] and row['results']['TitleMatchPicOCR']:

                row['results']['H3_Trust'] = True

        return data

