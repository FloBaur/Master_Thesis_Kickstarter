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

    def textMatch(self, phrases, Tags):

        result = None

        if len(Tags) > 0 and len(phrases) > 0:
            if bool(set(phrases) & set(Tags)):
                result = True

        return result

    def getCats(self, data):
        categories = []

        for row in data:
            categories.append(row['filter']['category'])

        setCat = set(categories)

        return setCat


