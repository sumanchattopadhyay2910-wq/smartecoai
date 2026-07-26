class PredictionEngine:
    def __init__(self, detector, tracker):
        self.detector = detector
        self.tracker = tracker

    def run(self, image_path: str):
        detections = self.detector.detect(image_path)
        tracked = self.tracker.update(detections)
        return {"detections": detections, "tracked": tracked}
