class Image:
    def __init__(self, x, y, url, start_time):
        self.x = x
        self.y = y
        self.url = url
        self.start_time = start_time

    def toString(self):
        print(f"Image: (x={self.x}, y={self.y}), URL: {self.url}, Start Time: {self.start_time}")