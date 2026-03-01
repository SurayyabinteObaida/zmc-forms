from flask import Blueprint, render_template
from app.models import FormType, ExtractedRecord, Submission, FlexoPrintingRecord, GravurePrintingRecord

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    form_types = FormType.query.all()
    total_submissions = Submission.query.count()
    total_records = ExtractedRecord.query.count()
    saved_records = ExtractedRecord.query.filter_by(status="saved").count()
    pending_records = ExtractedRecord.query.filter(
        ExtractedRecord.status.in_(["extracted", "verified"])
    ).count()

    recent_submissions = (
        Submission.query.order_by(Submission.uploaded_at.desc()).limit(10).all()
    )

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
    )