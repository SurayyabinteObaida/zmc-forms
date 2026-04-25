"""
upload.py  (V2)
────────────────────────────────────────────────────────────────────────────
Two-phase upload flow:

  POST /upload/process
    → Save files, classify each image (lightweight), return category summary.
      Records saved with status="classified". Submission status="classified".

  POST /upload/extract/<submission_id>/<form_type_code>
    → Trigger full extraction for all classified records of a given form type
      within a submission. Returns extracted record data.

  GET  /upload/
    → Upload screen (unchanged).

  GET  /upload/classify/<submission_id>
    → Category summary screen (new V2 screen).
"""

import os
import uuid
import json
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import FormType, Submission, ExtractedRecord
from app.services.extraction_service import classify_image, extract
from app.blueprints.auth import login_required

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Screens ───────────────────────────────────────────────────────────────────

@upload_bp.route("/", methods=["GET"])
@login_required
def index():
    return render_template("upload/index.html")


@upload_bp.route("/classify/<int:submission_id>", methods=["GET"])
@login_required
def classify_screen(submission_id):
    """Category summary screen — shown after classification completes."""
    submission = Submission.query.get_or_404(submission_id)
    records = ExtractedRecord.query.filter_by(submission_id=submission_id).all()

    # Group records by form type
    categories = {}
    unclassified = []

    for rec in records:
        if rec.form_type_id:
            ft = FormType.query.get(rec.form_type_id)
            if ft:
                key = ft.code
                if key not in categories:
                    categories[key] = {
                        "form_type": ft,
                        "records": [],
                        "error_count": 0,
                    }
                categories[key]["records"].append(rec)
                if rec.status == "error":
                    categories[key]["error_count"] += 1
            else:
                unclassified.append(rec)
        else:
            unclassified.append(rec)

    return render_template(
        "upload/classify.html",
        submission=submission,
        categories=categories,       # dict keyed by form_code
        unclassified=unclassified,
        total_count=len(records),
    )


# ── API: Phase 1 — Classify ───────────────────────────────────────────────────

@upload_bp.route("/process", methods=["POST"])
@login_required
def process():
    """
    Save uploaded files and classify each one.
    Returns classification summary; does NOT extract data yet.
    """
    files = request.files.getlist("files")
    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No files uploaded"}), 400

    batch_id = str(uuid.uuid4())
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], batch_id)
    os.makedirs(upload_dir, exist_ok=True)

    submission = Submission(batch_id=batch_id, status="classified")
    db.session.add(submission)
    db.session.flush()

    form_types = FormType.query.all()
    form_type_map = {ft.code: ft for ft in form_types}

    results = []

    for file in files:
        if not file or not _allowed_file(file.filename):
            continue

        filename = secure_filename(file.filename)
        image_path = os.path.join(upload_dir, filename)
        file.save(image_path)

        # Lightweight classification only
        classification = classify_image(image_path)

        form_code = classification["form_code"]
        matched_ft = form_type_map.get(form_code)

        record = ExtractedRecord(
            submission_id=submission.id,
            form_type_id=matched_ft.id if matched_ft else None,
            filename=filename,
            image_path=image_path,
            confidence=classification["confidence"],
            status="classified" if not classification["error"] else "error",
            error_message=classification["error"],
        )
        db.session.add(record)
        db.session.flush()

        results.append({
            "record_id": record.id,
            "filename": filename,
            "form_code": form_code,
            "form_name": classification["form_name"],
            "form_type_id": matched_ft.id if matched_ft else None,
            "confidence": classification["confidence"],
            "error": classification["error"],
        })

    db.session.commit()

    # Build category summary for frontend
    summary = _build_category_summary(results, form_type_map)

    return jsonify({
        "submission_id": submission.id,
        "batch_id": batch_id,
        "total": len(results),
        "summary": summary,
        "results": results,
    })


# ── API: Phase 2 — Extract ────────────────────────────────────────────────────

@upload_bp.route("/extract/<int:submission_id>/<path:form_type_code>", methods=["POST"])
@login_required
def extract_batch(submission_id, form_type_code):
    """
    Trigger full extraction for all classified records of a given form type
    in a submission. Skips records already extracted.
    """
    submission = Submission.query.get_or_404(submission_id)
    form_type = FormType.query.filter_by(code=form_type_code).first()

    if not form_type:
        return jsonify({"error": f"Unknown form type: {form_type_code}"}), 404

    records = ExtractedRecord.query.filter_by(
        submission_id=submission_id,
        form_type_id=form_type.id,
    ).all()

    if not records:
        return jsonify({"error": "No records found for this form type in this submission"}), 404

    extracted_results = []
    errors = []

    for rec in records:
        # Skip if already extracted or saved
        if rec.status in ("extracted", "saved"):
            extracted_results.append({
                "record_id": rec.id,
                "status": rec.status,
                "skipped": True,
            })
            continue

        result = extract(form_type_code, rec.image_path, form_type_obj=form_type)

        if result["error"]:
            rec.status = "error"
            rec.error_message = result["error"]
            errors.append({"record_id": rec.id, "error": result["error"]})
        else:
            rec.raw_extraction = json.dumps(result["data"])
            rec.confidence = result["confidence"]
            rec.status = "extracted"
            rec.error_message = None
            extracted_results.append({
                "record_id": rec.id,
                "status": "extracted",
                "skipped": False,
            })

    db.session.commit()

    return jsonify({
        "submission_id": submission_id,
        "form_type_code": form_type_code,
        "extracted": len([r for r in extracted_results if not r.get("skipped")]),
        "skipped": len([r for r in extracted_results if r.get("skipped")]),
        "errors": errors,
        "results": extracted_results,
    })


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_category_summary(results: list, form_type_map: dict) -> list:
    """Group classification results into a summary list per form type."""
    groups = {}
    for r in results:
        code = r["form_code"]
        if code not in groups:
            groups[code] = {
                "form_code": code,
                "form_name": r["form_name"],
                "form_type_id": r["form_type_id"],
                "count": 0,
                "error_count": 0,
            }
        groups[code]["count"] += 1
        if r["error"]:
            groups[code]["error_count"] += 1

    return list(groups.values())