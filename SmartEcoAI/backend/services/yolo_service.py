class YOLOService:
    def __init__(self, model_path: str | None = None):
        self.model_path = model_path

    def predict(self, image_path: str):
        return {
            "image_path": image_path,
            "status": "model-ready",
            "message": "YOLO integration placeholder. Replace with real model inference.",
        }
