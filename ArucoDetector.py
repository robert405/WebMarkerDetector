import cv2
import cv2.aruco as aruco
import numpy as np
from imgaug import augmenters as iaa

class ArucoDetector:

    def __init__(self):

        self.arucoDict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        self.parameters = aruco.DetectorParameters_create()

    def detect(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.arucoDict, parameters=self.parameters)

        if (ids is None):
            raise ValueError('Found no markers!')
        elif (len(ids) < 4):
            raise ValueError("Found only " + str(len(ids)) + " markers, 4 are needed!")

        return self.calculateMarkerMeanPos(corners)

    def detectAndCorrect(self, img):

        try :

            ar = self.detect(img)
            return ar

        except :

            modifList = []
            modifList += [iaa.ContrastNormalization(1.6)]
            modifList += [iaa.Add(-65)]
            modifList += [iaa.Sharpen(alpha=0.7, lightness=1)]

            for modif in modifList:

                try :

                    modifImg = modif.augment_image(img)
                    ar = self.detect(modifImg)
                    return ar

                except :
                    pass

        raise ValueError('Not enough markers!')

    def calculateMarkerMeanPos(self, corners):

        markerList = []
        for element in corners:

            marker = element[0]
            x = 0
            y = 0

            for corner in marker:
                x += corner[0]
                y += corner[1]

            x = int(x / 4)
            y = int(y / 4)

            markerList += [(x, y)]

        return np.array(markerList)

    def calculateBigFrameContour(self, markerList):

        minX = 999999999
        minY = 999999999
        maxX = 0
        maxY = 0

        for pos in markerList:

            if (pos[0] < minX):
                minX = int(pos[0])

            if (pos[0] > maxX):
                maxX = int(pos[0])

            if (pos[1] < minY):
                minY = int(pos[1])

            if (pos[1] > maxY):
                maxY = int(pos[1])

        return (minX, minY), (maxX, maxY)

    def calculateSmallFrameContour(self, markerList):

        allX = []
        allY = []

        for pos in markerList:

            allX += [pos[0]]
            allY += [pos[1]]

        allX.sort()
        allY.sort()

        return (int(allX[1]), int(allY[1])), (int(allX[len(allX)-2]), int(allY[len(allY)-2]))

    def createMarkers(self, nbMarker, markerRes, whiteBorder, blackBorder):

        markerList = []
        border = whiteBorder + blackBorder
        totalSize = markerRes + (2 * border)


        for i in range(1, nbMarker+1):

            whiteBackground = np.ones((totalSize,totalSize)) * 255
            whiteBackground[0:blackBorder,:] = 0
            whiteBackground[totalSize-blackBorder:totalSize,:] = 0
            whiteBackground[:,0:blackBorder] = 0
            whiteBackground[:,totalSize-blackBorder:totalSize] = 0
            marker = aruco.drawMarker(self.arucoDict, i, markerRes)
            whiteBackground[border:totalSize-border,border:totalSize-border] = marker
            markerList += [whiteBackground]

        return markerList

    def getRejectionInfo(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.arucoDict, parameters=self.parameters)

        if (ids is None):
            raise ValueError('Found no markers!')

        canvas = np.zeros_like(img)
        canvas = aruco.drawDetectedMarkers(canvas, rejectedImgPoints)

        return canvas, self.calculateMarkerMeanPos(ids, corners)