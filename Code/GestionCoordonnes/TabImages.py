from Image import Image
import time


class TabImages:
    def __init__(self, images=None,
                 x_init=100.0,
                 y_init=100.0,
                 image_width=350.0,
                 image_height=350.0,
                 tab_width=1200.0,
                 tab_height=900.0,
                 spacing_h=10.0,
                 spacing_v=10.0,
                 ordering=True,
                 timeout=60.0):

        if images is None:
            self.listImages = []
        else:
            self.listImages = images
        self.x_init = x_init
        self.y_init = y_init
        self.image_width = image_width
        self.image_height = image_height
        self.tab_width = tab_width
        self.tab_height = tab_height
        self.spacing_h = spacing_h
        self.spacing_v = spacing_v
        self.ordering = ordering
        self.timeout = timeout  # seconds

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
                listPla.append((x + 0.0, y + 0.0))
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
            older = self.getOlderImage()
            self.removeImgToList(older)
            x = older.x
            y = older.y
        return x, y

    def getOlderImage(self):
        older = self.listImages[-1]
        for img in self.listImages:
            if img.start_time < older.start_time:
                older = img
        return older

    def order(self):
        if self.ordering is True:
            sorted_images = sorted(self.listImages, key=lambda im: im.start_time)
            places = self.getAllPlaces()
            cpt = 0
            for image in sorted_images:
                (x, y) = places[cpt]
                image.x = x
                image.y = y
                cpt += 1

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
