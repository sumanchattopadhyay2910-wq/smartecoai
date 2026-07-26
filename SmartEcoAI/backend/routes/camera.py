import base64
import mimetypes
from pathlib import Path

from flask import Blueprint, current_app, render_template, request

from backend.services.camera_service import CameraService
from backend.services.gemini_service import GeminiService, analysis_to_dict
from backend.utils.validator import is_allowed_file

camera_bp = Blueprint("camera", __name__)


@camera_bp.route("/camera", methods=["GET", "POST"])
def camera():
    analysis = None
    preview_image = None
    uploaded_name = None
    error = None

    if request.method == "POST":
        file_storage = request.files.get("photo")
        if not file_storage or not file_storage.filename:
            error = "Please choose an image to analyze."
        elif not is_allowed_file(file_storage.filename, {"png", "jpg", "jpeg", "webp"}):
            error = "Please upload a PNG, JPG, JPEG, or WEBP image."
        else:
            camera_service = CameraService(current_app.config["UPLOAD_FOLDER"])
            saved_path = camera_service.save_upload(file_storage)
            uploaded_name = Path(saved_path).name

            image_bytes = Path(saved_path).read_bytes()
            mime_type = file_storage.mimetype or mimetypes.guess_type(saved_path)[0] or "image/jpeg"
            preview_image = f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"

            gemini_service = GeminiService(
                api_key=current_app.config["GEMINI_API_KEY"],
                model=current_app.config["GEMINI_MODEL"],
            )
            analysis = analysis_to_dict(
                gemini_service.analyze_image(
                    image_bytes=image_bytes,
                    mime_type=mime_type,
                    filename=file_storage.filename,
                )
            )

    return render_template(
        "camera.html",
        analysis=analysis,
        preview_image=preview_image,
        uploaded_name=uploaded_name,
        error=error,
    )
