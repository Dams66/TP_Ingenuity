from Image import Image
import time


class TabImages:
    def __init__(self, images=None):
        if images is None:
            self.listImages = []
        else:
            self.listImages = images
        self.x_init = 100.0
        self.y_init = 100.0
        self.image_width = 350.0
        self.image_height = 350.0
        self.tab_width = 1200.0
        self.tab_height = 900.0
        self.spacing_h = 10.0
        self.spacing_v = 10.0
        self.timeout = 30.0  # seconds

    def addImgToList(self, image):
        self.listImages.append(image)

    def removeImgToList(self, image):
        self.listImages.remove(image)

    def getImageFromCoord(self, x, y):
        res = None
        for img in self.listImages:
            if (img.x == x) and (img.y == y):
                res = img
        if res is None:
            print('Pas d\'images correspondantes pour ces coordonnees')
        return res

    def getAllPlaces(self):
        listPla = []
        x = self.x_init
        y = self.y_init
        for y in range(int(self.y_init), int(self.tab_height), int(self.spacing_v) + int(self.image_height)):
            for x in range(int(self.x_init), int(self.tab_width), int(self.spacing_h) + int(self.image_width)):
                listPla.append((x+0.0, y+0.0))
        return listPla

    def isFree(self, x, y):
        res = True
        for img in self.listImages:
            if (img.x == x) and (img.y == y):
                res = False
        return res

    def closerFree(self):
        if not self.listImages:
            x = self.x_init
            y = self.y_init
        else:
            listPlace = self.getAllPlaces()
            for (x, y) in listPlace:
                if self.isFree(x, y):
                    return x, y
            self.removeImgToList(self.getImageFromCoord(self.x_init, self.y_init))
            x = self.x_init
            y = self.y_init
        return x, y

    def checkTimeout(self):
        listTimeOut = []
        for img in self.listImages:
            if isinstance(img, Image):
                if time.time() - img.start_time > self.timeout:
                    listTimeOut.append(img)
            else:
                print("Error")
        return listTimeOut

    def deleteTimeout(self):
        listTO = self.checkTimeout()
        for i in listTO:
            self.removeImgToList(i)

    def toString(self):
        for img in self.listImages:
            img.toString()