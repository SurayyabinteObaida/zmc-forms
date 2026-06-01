from flask import Blueprint, render_template, jsonify, session, redirect, url_for, request
from app import db
from app.models import FormType, ExtractedRecord, Submission, FlexoPrintingRecord, GravurePrintingRecord
from app.blueprints.auth import login_required

main_bp = Blueprint("main", __name__)


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
    recent_submissions = pagination.items

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
        recent_submissions=recent_submissions,
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