from flask import Blueprint, send_file, jsonify
import io
from app.models import FormType, ExtractedRecord
from app.services.excel_service import generate_excel
from app.blueprints.auth import login_required

export_bp = Blueprint("export", __name__)


@export_bp.route("/excel/<int:form_type_id>")
@login_required
def export_excel(form_type_id):
    ft = FormType.query.get_or_404(form_type_id)
    records = (
        ExtractedRecord.query
        .filter_by(form_type_id=form_type_id, status="saved")
        .order_by(ExtractedRecord.saved_at.desc())
        .all()
    )

    if not records:
        return jsonify({"error": "No saved records found for this form type"}), 404

    xlsx_bytes = generate_excel(ft, records)
    safe_name = ft.name.replace(" ", "_").replace("/", "-")
    return send_file(
        io.BytesIO(xlsx_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=f"{safe_name}_export.xlsx",
    )