class Tracker:
    def __init__(self):
        self.objects = {}

    def update(self, detections):
        self.objects = {str(i): detection for i, detection in enumerate(detections)}
        return self.objects
