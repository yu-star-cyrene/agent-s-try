import json
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from src.core.types import InspectionRequest
from src.main import build_default_pipeline


PIPELINE = build_default_pipeline()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _sample_payload() -> dict:
    sample_path = _project_root() / "data" / "samples" / "request_example.json"
    return json.loads(sample_path.read_text(encoding="utf-8"))


def _save_uploaded_file(file_storage) -> str:
    uploads_dir = _project_root() / "data" / "raw" / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    original_name = secure_filename(file_storage.filename or "upload.bin")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_name = f"{timestamp}_{original_name}" if original_name else f"{timestamp}_upload.bin"
    saved_path = uploads_dir / saved_name
    file_storage.save(saved_path)
    return str(saved_path)


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    @app.route("/", methods=["GET", "POST"])
    def index():
        sample = _sample_payload()
        form_data = {
            "parcel_id": sample.get("parcel_id", ""),
            "image_path": sample.get("image_path", ""),
            "land_type": sample.get("land_type", ""),
            "text_description": sample.get("text_description", ""),
            "rules": "\n".join(sample.get("rules", [])),
        }
        result = None
        error = None

        if request.method == "POST":
            form_data = {
                "parcel_id": request.form.get("parcel_id", "").strip(),
                "image_path": request.form.get("image_path", "").strip(),
                "land_type": request.form.get("land_type", "").strip(),
                "text_description": request.form.get("text_description", "").strip(),
                "rules": request.form.get("rules", "").strip(),
            }

            upload = request.files.get("image_file")
            if upload and upload.filename:
                form_data["image_path"] = _save_uploaded_file(upload)

            try:
                rules = [
                    line.strip()
                    for line in form_data["rules"].splitlines()
                    if line.strip()
                ]
                inspection_request = InspectionRequest(
                    parcel_id=form_data["parcel_id"] or "UNNAMED-PARCEL",
                    image_path=form_data["image_path"] or "未提供图片路径",
                    text_description=form_data["text_description"],
                    land_type=form_data["land_type"],
                    rules=rules,
                    metadata={"source": "web-ui"},
                )
                result = PIPELINE.run(inspection_request)
            except Exception as exc:
                error = f"页面分析失败：{exc}"

        return render_template(
            "index.html",
            form_data=form_data,
            result=result.to_dict() if result else None,
            error=error,
        )

    return app
