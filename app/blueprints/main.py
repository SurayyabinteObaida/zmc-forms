import json
from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request
from app import db
from app.models import FormType, ExtractedRecord, Submission, FlexoPrintingRecord, GravurePrintingRecord
from app.blueprints.auth import login_required

main_bp = Blueprint("main", __name__)

FORM_TYPE_SHORT = {
    "F-PRD/01.2": "Flexo",
    "F-PRD/01.1": "Gravure",
    "F-PRD/02.1": "Lamination",
    "F-PRD/03.1": "Slitting",
}

FORM_TYPE_COLOR = {
    "F-PRD/01.2": "#2E75B6",
    "F-PRD/01.1": "#7C3AED",
    "F-PRD/02.1": "#059669",
    "F-PRD/03.1": "#D97706",
}

DATE_KEYS = ("date", "print_date")


def _enrich_submissions(submissions):
    form_type_map = {ft.id: ft for ft in FormType.query.all()}
    enriched = []
    for sub in submissions:
        form_types_seen = {}
        job_names = []
        dates = []
        for rec in sub.records:
            ft = form_type_map.get(rec.form_type_id)
            if ft and ft.code not in form_types_seen:
                form_types_seen[ft.code] = ft
            raw = rec.verified_data or rec.raw_extraction
            if raw:
                try:
                    data = json.loads(raw)
                    job = data.get("job_name")
                    if job and job not in job_names:
                        job_names.append(job)
                    for dk in DATE_KEYS:
                        if data.get(dk):
                            dates.append(data[dk])
                            break
                except Exception:
                    pass
        enriched.append({
            "sub": sub,
            "form_types": list(form_types_seen.values()),
            "job_names": job_names[:3],
            "date": dates[0] if dates else None,
        })
    return enriched


@main_bp.route("/")
@login_required
def dashboard():
    form_types = FormType.query.all()
    total_submissions = Submission.query.count()
    total_records = ExtractedRecord.query.count()
    saved_records = ExtractedRecord.query.filter_by(status="saved").count()
    pending_records = ExtractedRecord.query.filter(
        ExtractedRecord.status.in_(["extracted", "verified"])
    ).count()

    page = request.args.get("page", 1, type=int)
    pagination = (
        Submission.query.order_by(Submission.uploaded_at.desc())
        .paginate(page=page, per_page=10, error_out=False)
    )
    enriched_submissions = _enrich_submissions(pagination.items)

    stats = {
        "total_submissions": total_submissions,
        "total_records": total_records,
        "saved_records": saved_records,
        "pending_records": pending_records,
        "flexo_count": FlexoPrintingRecord.query.count(),
        "gravure_count": GravurePrintingRecord.query.count(),
    }

    return render_template(
        "dashboard/index.html",
        form_types=form_types,
        stats=stats,
        enriched_submissions=enriched_submissions,
        form_type_short=FORM_TYPE_SHORT,
        form_type_color=FORM_TYPE_COLOR,
        pagination=pagination,
    )


@main_bp.route("/delete-submission/<int:submission_id>", methods=["DELETE"])
@login_required
def delete_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    records = ExtractedRecord.query.filter_by(submission_id=submission_id).all()

    for rec in records:
        form_type = FormType.query.get(rec.form_type_id) if rec.form_type_id else None
        if form_type:
            if form_type.code == "F-PRD/01.2":
                FlexoPrintingRecord.query.filter_by(extracted_record_id=rec.id).delete()
            elif form_type.code == "F-PRD/01.1":
                GravurePrintingRecord.query.filter_by(extracted_record_id=rec.id).delete()
        db.session.delete(rec)

    db.session.delete(submission)
    db.session.commit()
    return jsonify({"success": True})