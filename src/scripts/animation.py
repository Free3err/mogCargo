class Animation:
    def __init__(self, images, fps):
        self.images = images
        self.fps = fps
        self.current_image = 0

    def update(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        return self.images[self.current_image]

