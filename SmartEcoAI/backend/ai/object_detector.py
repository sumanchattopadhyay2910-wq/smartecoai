class ObjectDetector:
    def __init__(self, model_path: str | None = None):
        self.model_path = model_path

    def detect(self, image_path: str):
        return [
            {"label": "person", "confidence": 0.92, "bbox": [0, 0, 100, 100]},
        ]
