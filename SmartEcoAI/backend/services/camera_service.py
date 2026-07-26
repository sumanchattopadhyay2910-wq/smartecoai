from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename


class CameraService:
    def __init__(self, upload_dir: str | None = None):
        self.upload_dir = Path(upload_dir or "uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, file_storage) -> str:
        original_name = secure_filename(file_storage.filename or "upload")
        suffix = Path(original_name).suffix
        stem = Path(original_name).stem or "upload"
        filename = f"{stem}_{uuid4().hex[:8]}{suffix}"
        destination = self.upload_dir / filename
        file_storage.save(destination)
        return str(destination)
