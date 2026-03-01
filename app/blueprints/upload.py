import os
import uuid
import json
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import FormType, Submission, ExtractedRecord
from app.services.extraction_service import process_image

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/", methods=["GET"])
def index():
    return render_template("upload/index.html")


@upload_bp.route("/process", methods=["POST"])
def process():
    """
    Receives uploaded images, runs AI extraction on each,
    creates a Submission + ExtractedRecord rows, returns batch_id.
    """
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No files uploaded"}), 400

    batch_id = str(uuid.uuid4())
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], batch_id)
    os.makedirs(upload_dir, exist_ok=True)

    submission = Submission(batch_id=batch_id, status="pending")
    db.session.add(submission)
    db.session.flush()

    form_types = FormType.query.all()
    results = []

    for file in files:
        if not file or not _allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        image_path = os.path.join(upload_dir, filename)
        file.save(image_path)

        # Run AI extraction pipeline
        result = process_image(image_path, form_types)

        record = ExtractedRecord(
            submission_id=submission.id,
            form_type_id=result["form_type_id"],
            filename=filename,
            image_path=image_path,
            raw_extraction=json.dumps(result["data"]),
            confidence=result["confidence"],
            status="extracted" if not result["error"] else "error",
            error_message=result["error"],
        )
        db.session.add(record)
        db.session.flush()

        results.append({
            "record_id": record.id,
            "filename": filename,
            "form_code": result["form_code"],
            "form_type_id": result["form_type_id"],
            "confidence": result["confidence"],
            "error": result["error"],
        })

    submission.status = "extracted"
    db.session.commit()

    return jsonify({"batch_id": batch_id, "submission_id": submission.id, "results": results})