class TabImages:
    def __init__(self, images=None):
        if images is None:
            self.listImages = []
        else:
            self.listImages = images
        self.image_width = 350.0
        self.image_height = 350.0
        self.tab_length = 1200.0
        self.tab_height = 900.0
        self.spacing_h = 10.0
        self.spacing_v = 10.0
        self.timeout = 30.0  # seconds

    def addImgToList(self, image):
        self.listImages.append(image)
