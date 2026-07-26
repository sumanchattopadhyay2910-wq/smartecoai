from pathlib import Path


class ModelLoader:
    def __init__(self, model_path: str | None = None):
        self.model_path = Path(model_path or "models/yolov11.pt")

    def exists(self) -> bool:
        return self.model_path.exists()
