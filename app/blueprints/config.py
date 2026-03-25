from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import FormType, FieldConfig
from app.blueprints.auth import login_required

config_bp = Blueprint("config", __name__)


@config_bp.route("/")
@login_required
def index():
    form_types = FormType.query.all()
    return render_template("field_config/index.html", form_types=form_types)


@config_bp.route("/fields/<int:form_type_id>", methods=["GET"])
@login_required
def get_fields(form_type_id):
    ft = FormType.query.get_or_404(form_type_id)
    fields = [f.to_dict() for f in ft.field_configs]
    return jsonify({"form_type": {"id": ft.id, "name": ft.name, "code": ft.code}, "fields": fields})


@config_bp.route("/save/<int:form_type_id>", methods=["POST"])
@login_required
def save_config(form_type_id):
    """Save field configuration changes - matches field_config/index.html JavaScript."""
    ft = FormType.query.get_or_404(form_type_id)
    payload = request.get_json()
    
    if not payload:
        return jsonify({"success": False, "error": "No data received"}), 400
    
    updates = payload.get("fields", {})  # {field_id_str: enabled_bool}
    
    if not updates:
        return jsonify({"success": False, "error": "No fields in payload"}), 400
    
    updated_count = 0
    
    for field_id_str, enabled in updates.items():
        try:
            field_id = int(field_id_str)
            fc = FieldConfig.query.get(field_id)
            
            # Verify field belongs to this form type
            if fc and fc.form_type_id == form_type_id:
                fc.enabled = bool(enabled)
                updated_count += 1
        except (ValueError, TypeError) as e:
            # Skip invalid field IDs
            continue
    
    db.session.commit()
    return jsonify({"success": True, "updated": updated_count})


@config_bp.route("/fields/<int:form_type_id>", methods=["POST"])
@login_required
def update_fields(form_type_id):
    """Bulk update field enabled/order/label for a form type."""
    FormType.query.get_or_404(form_type_id)
    payload = request.get_json()
    updates = payload.get("fields", [])  # [{id, enabled, label, order}]

    for upd in updates:
        fc = FieldConfig.query.get(upd["id"])
        if fc and fc.form_type_id == form_type_id:
            fc.enabled = upd.get("enabled", fc.enabled)
            fc.label = upd.get("label", fc.label)
            fc.order = upd.get("order", fc.order)

    db.session.commit()
    return jsonify({"success": True, "updated": len(updates)})


@config_bp.route("/fields/toggle", methods=["POST"])
@login_required
def toggle_field():
    payload = request.get_json()
    fc = FieldConfig.query.get_or_404(payload["field_id"])
    fc.enabled = not fc.enabled
    db.session.commit()
    return jsonify({"success": True, "field_id": fc.id, "enabled": fc.enabled})