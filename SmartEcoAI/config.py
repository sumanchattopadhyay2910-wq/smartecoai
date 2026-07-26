import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "smart-eco-ai-secret")
    UPLOAD_FOLDER = str(BASE_DIR / "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "mp4", "mov"}
    DATABASE_PATH = str(BASE_DIR / "instance" / "smarteco.db")
    MODEL_PATH = str(BASE_DIR / "models" / "yolov11.pt")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
