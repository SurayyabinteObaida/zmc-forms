from datetime import datetime, timezone
from app import db


class FormType(db.Model):
    """Represents a form category (e.g. Flexo Printing, Gravure Printing)."""
    __tablename__ = "form_types"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    keywords = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    field_configs = db.relationship("FieldConfig", back_populates="form_type",
                                    cascade="all, delete-orphan", order_by="FieldConfig.order")

    def keywords_list(self):
        return [k.strip().lower() for k in (self.keywords or "").split(",") if k.strip()]

    def enabled_fields(self):
        return [f for f in self.field_configs if f.enabled]


class FieldConfig(db.Model):
    """Configures which fields are active for a given form type."""
    __tablename__ = "field_configs"

    id = db.Column(db.Integer, primary_key=True)
    form_type_id = db.Column(db.Integer, db.ForeignKey("form_types.id"), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    field_type = db.Column(db.String(50), default="text")
    enabled = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)

    form_type = db.relationship("FormType", back_populates="field_configs")

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "label": self.label,
            "field_type": self.field_type,
            "enabled": self.enabled,
            "order": self.order,
        }


class Submission(db.Model):
    """A batch upload session containing one or more form images."""
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(100), unique=True, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # V2 status lifecycle: pending → classified → extracted → verified → saved
    status = db.Column(db.String(50), default="pending")

    records = db.relationship("ExtractedRecord", back_populates="submission",
                              cascade="all, delete-orphan")


class ExtractedRecord(db.Model):
    """One extracted form's data within a submission batch."""
    __tablename__ = "extracted_records"

    id = db.Column(db.Integer, primary_key=True)
    submission_id = db.Column(db.Integer, db.ForeignKey("submissions.id"), nullable=False)
    form_type_id = db.Column(db.Integer, db.ForeignKey("form_types.id"), nullable=True)

    filename = db.Column(db.String(300), nullable=True)
    image_path = db.Column(db.String(500), nullable=True)

    raw_extraction = db.Column(db.Text, nullable=True)
    verified_data = db.Column(db.Text, nullable=True)

    # V2 status lifecycle: classified → extracted → verified → saved | error
    status = db.Column(db.String(50), default="classified")
    error_message = db.Column(db.Text, nullable=True)
    confidence = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    saved_at = db.Column(db.DateTime, nullable=True)

    submission = db.relationship("Submission", back_populates="records")
    form_type = db.relationship("FormType", foreign_keys=[form_type_id])


# ── Typed storage tables ──────────────────────────────────────────────────────

class FlexoPrintingRecord(db.Model):
    """Permanent typed storage for verified Flexo Printing records."""
    __tablename__ = "flexo_printing_records"

    id = db.Column(db.Integer, primary_key=True)
    extracted_record_id = db.Column(db.Integer, db.ForeignKey("extracted_records.id"), unique=True)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    date = db.Column(db.String(50))
    job_name = db.Column(db.String(200))
    job_code = db.Column(db.String(100))
    party_name = db.Column(db.String(200))
    operator = db.Column(db.String(200))
    material = db.Column(db.String(200))
    supplier = db.Column(db.String(200))
    rm_number = db.Column(db.String(100))
    order_qty = db.Column(db.Float)
    web_size = db.Column(db.String(100))
    mic = db.Column(db.String(100))
    cylinder_size = db.Column(db.String(100))
    no_of_colors = db.Column(db.Float)
    ink_gsm = db.Column(db.Float)
    speed = db.Column(db.Float)
    block_number = db.Column(db.String(100))
    tube_sheet = db.Column(db.String(100))
    bag_size = db.Column(db.String(100))
    setting_time = db.Column(db.String(100))
    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))
    plain_roll_wt = db.Column(db.Float)
    plain_bal = db.Column(db.Float)
    printed_roll_number = db.Column(db.String(200))
    printed_reel_wt = db.Column(db.Float)
    core_wt = db.Column(db.Float)
    counter_meter = db.Column(db.String(200))
    balance_rejected = db.Column(db.String(200))
    gross_wt = db.Column(db.Float)
    net_wt = db.Column(db.Float)
    total_counter = db.Column(db.Float)
    total_meter = db.Column(db.Float)
    setting_waste = db.Column(db.Float)
    roll_waste = db.Column(db.Float)
    printed_waste = db.Column(db.Float)
    plain_waste = db.Column(db.Float)
    total_waste = db.Column(db.Float)
    rejected_core_wt = db.Column(db.Float)
    prepared_by = db.Column(db.String(200))
    supervisor = db.Column(db.String(200))
    remarks = db.Column(db.Text)


class GravurePrintingRecord(db.Model):
    """Permanent typed storage for verified Gravure Printing records."""
    __tablename__ = "gravure_printing_records"

    id = db.Column(db.Integer, primary_key=True)
    extracted_record_id = db.Column(db.Integer, db.ForeignKey("extracted_records.id"), unique=True)
    saved_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # ── Header fields ─────────────────────────────────────────────────────────
    print_date = db.Column(db.String(50))
    job_name = db.Column(db.String(200))
    job_code = db.Column(db.String(100))
    plain_order_qty = db.Column(db.Float)
    material = db.Column(db.String(200))
    material_supplier = db.Column(db.String(200))
    web_size_mic = db.Column(db.String(200))
    cylinder_qty_number = db.Column(db.String(200))
    cylinder_length_cir = db.Column(db.String(200))
    speed = db.Column(db.Float)
    operator = db.Column(db.String(200))
    color_man = db.Column(db.String(200))
    ink_gsm = db.Column(db.Float)
    setting_time = db.Column(db.String(100))
    start_time = db.Column(db.String(100))
    end_time = db.Column(db.String(100))

    # ── Footer / summary fields ───────────────────────────────────────────────
    plain_gross_wt = db.Column(db.Float)
    printed_gross_wt = db.Column(db.Float)
    plain_core_wt = db.Column(db.Float)
    printed_core_wt = db.Column(db.Float)
    plain_balance = db.Column(db.Float)
    plain_net_wt = db.Column(db.Float)
    printed_net_wt = db.Column(db.Float)
    total_mtr = db.Column(db.Float)
    plain_waste = db.Column(db.Float)
    roll_waste = db.Column(db.Float)
    printed_waste = db.Column(db.Float)
    setting_waste = db.Column(db.Float)
    total_waste = db.Column(db.Float)

    # ── Signatures ────────────────────────────────────────────────────────────
    prepared_by = db.Column(db.String(200))
    supervisor = db.Column(db.String(200))
    remarks = db.Column(db.Text)