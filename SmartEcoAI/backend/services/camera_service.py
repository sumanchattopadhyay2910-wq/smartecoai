from pathlib import Path


class CameraService:
    def __init__(self, upload_dir: str | None = None):
        self.upload_dir = Path(upload_dir or "uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_storage) -> str:
        filename = file_storage.filename or "upload"
        destination = self.upload_dir / filename
        file_storage.save(destination)
        return str(destination)
