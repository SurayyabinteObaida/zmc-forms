import json
from datetime import datetime, timezone
from io import BytesIO
from flask import Blueprint, render_template, request, jsonify, send_file
from app import db
from app.services.excel_service import (generate_batch_excel,
    get_column_config_for_ui, save_export_config)
from app.models import (FormType, ExtractedRecord, Submission,
                         FlexoPrintingRecord, GravurePrintingRecord)
from app.blueprints.auth import login_required

verify_bp = Blueprint("verify", __name__)

FORM_MODEL_MAP = {
    "F-PRD/01.2": FlexoPrintingRecord,
    "F-PRD/01.1": GravurePrintingRecord,
}


@verify_bp.route("/<int:submission_id>")
@login_required
def index(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    records = ExtractedRecord.query.filter_by(submission_id=submission_id).all()

    enriched = []
    for rec in records:
        form_type = FormType.query.get(rec.form_type_id) if rec.form_type_id else None
        raw_data = json.loads(rec.raw_extraction or "{}")
        enabled_fields = form_type.enabled_fields() if form_type else []
        
        # Extract corrections if available
        corrections = {}
        if hasattr(rec, 'corrections_json'):
            try:
                corrections = json.loads(rec.corrections_json or "{}")
            except:
                pass
        
        enriched.append({
            "record": rec,
            "form_type": form_type,
            "raw_data": raw_data,
            "enabled_fields": enabled_fields,
            "corrections": corrections,
        })

    form_types_all = FormType.query.all()
    return render_template("verify/index.html", submission=submission, enriched=enriched, form_types=form_types_all)


@verify_bp.route("/record/<int:record_id>", methods=["GET"])
@login_required
def get_record(record_id):
    rec = ExtractedRecord.query.get_or_404(record_id)
    form_type = FormType.query.get(rec.form_type_id) if rec.form_type_id else None
    data = json.loads(rec.raw_extraction or "{}")
    fields = [f.to_dict() for f in form_type.enabled_fields()] if form_type else []

    return jsonify({
        "record_id": rec.id,
        "filename": rec.filename,
        "form_code": form_type.code if form_type else None,
        "form_name": form_type.name if form_type else "Unknown",
        "confidence": rec.confidence,
        "status": rec.status,
        "error": rec.error_message,
        "fields": fields,
        "data": data,
        "image_path": rec.image_path,
    })


@verify_bp.route("/save/<int:record_id>", methods=["POST"])
@login_required
def save_record(record_id):
    rec = ExtractedRecord.query.get_or_404(record_id)
    form_type = FormType.query.get(rec.form_type_id) if rec.form_type_id else None

    if not form_type:
        return jsonify({"error": "Unknown form type — cannot save"}), 400

    payload = request.get_json()
    verified_data = payload.get("data", {})

    rec.verified_data = json.dumps(verified_data)
    rec.status = "saved"
    rec.saved_at = datetime.now(timezone.utc)

    ModelClass = FORM_MODEL_MAP.get(form_type.code)
    if ModelClass:
        existing = ModelClass.query.filter_by(extracted_record_id=rec.id).first()
        if existing:
            db.session.delete(existing)
            db.session.flush()

        typed = ModelClass(extracted_record_id=rec.id)
        for key, value in verified_data.items():
            if hasattr(typed, key):
                setattr(typed, key, value if value != "" else None)
        db.session.add(typed)

    db.session.commit()
    return jsonify({"success": True, "record_id": rec.id, "status": rec.status})


@verify_bp.route("/save-batch/<int:submission_id>", methods=["POST"])
@login_required
def save_batch(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    payload = request.get_json()
    records_data = payload.get("records", {})

    saved_ids = []
    errors = []

    for rid_str, verified_data in records_data.items():
        rid = int(rid_str)
        rec = ExtractedRecord.query.get(rid)
        if not rec:
            errors.append(f"Record {rid} not found")
            continue

        form_type = FormType.query.get(rec.form_type_id) if rec.form_type_id else None
        if not form_type:
            errors.append(f"Record {rid}: unknown form type")
            continue

        rec.verified_data = json.dumps(verified_data)
        rec.status = "saved"
        rec.saved_at = datetime.now(timezone.utc)

        ModelClass = FORM_MODEL_MAP.get(form_type.code)
        if ModelClass:
            existing = ModelClass.query.filter_by(extracted_record_id=rec.id).first()
            if existing:
                db.session.delete(existing)
                db.session.flush()
            typed = ModelClass(extracted_record_id=rec.id)
            for key, value in verified_data.items():
                if hasattr(typed, key):
                    setattr(typed, key, value if value != "" else None)
            db.session.add(typed)

        saved_ids.append(rid)

    submission.status = "saved"
    db.session.commit()

    return jsonify({"success": True, "saved": saved_ids, "errors": errors})


@verify_bp.route("/update-form-type/<int:record_id>", methods=["POST"])
@login_required
def update_form_type(record_id):
    rec = ExtractedRecord.query.get_or_404(record_id)
    payload = request.get_json()
    form_type_id = payload.get("form_type_id")
    rec.form_type_id = form_type_id
    db.session.commit()
    return jsonify({"success": True})


@verify_bp.route("/export-batch/<int:submission_id>", methods=["GET"])
@login_required
def export_batch(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    record_id = request.args.get("record_id", type=int)

    # Fetch records
    if record_id:
        records = ExtractedRecord.query.filter_by(
            submission_id=submission_id,
            id=record_id
        ).all()
    else:
        records = ExtractedRecord.query.filter_by(
            submission_id=submission_id
        ).all()

    if not records:
        return jsonify({"error": "No records found"}), 404

    try:
        xlsx_bytes = generate_batch_excel(
            batch_id=str(submission_id),
            records=records
        )
        output = BytesIO(xlsx_bytes)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name=f"batch_{submission_id}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@verify_bp.route("/export-columns", methods=["GET"])
@login_required
def get_export_columns():
    return jsonify(get_column_config_for_ui())


@verify_bp.route("/export-columns", methods=["POST"])
@login_required
def save_export_columns():
    payload = request.get_json()
    if not isinstance(payload, dict):
        return jsonify({"error": "Expected a JSON object"}), 400
    save_export_config(payload)
    return jsonify({"success": True})