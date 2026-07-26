from pathlib import Path


class ImageService:
    def ensure_directory(self, directory: str) -> Path:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
