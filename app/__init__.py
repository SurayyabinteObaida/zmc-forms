import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Config ───────────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PERMANENT_SESSION_LIFETIME"] = 3600 * 8  # 8 hours

    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/zmc_forms")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", 50)) * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # ── Extensions ────────────────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)

    # ── Blueprints ────────────────────────────────────────────────────────────
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.upload import upload_bp
    from app.blueprints.verify import verify_bp
    from app.blueprints.config import config_bp
    from app.blueprints.export import export_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(verify_bp, url_prefix="/verify")
    app.register_blueprint(config_bp, url_prefix="/config")
    app.register_blueprint(export_bp, url_prefix="/export")

    # ── Seed default form types on first run ─────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_form_types()

    return app


def _seed_form_types():
    from app.models import FormType, FieldConfig

    forms = [
        {
            "code": "F-PRD/01.2",
            "name": "Flexo Printing Production Report",
            "keywords": ["flexo", "F-PRD/01.2", "flexo printing"],
            "fields": [
                {"key": "date",                "label": "Print Date",          "field_type": "date",   "enabled": True,  "order": 1},
                {"key": "job_name",            "label": "Job Name",            "field_type": "text",   "enabled": True,  "order": 2},
                {"key": "job_code",            "label": "Job Code",            "field_type": "text",   "enabled": True,  "order": 3},
                {"key": "party_name",          "label": "Party Name",          "field_type": "text",   "enabled": False, "order": 4},
                {"key": "operator",            "label": "Operator",            "field_type": "text",   "enabled": True,  "order": 5},
                {"key": "material",            "label": "Printed Film",        "field_type": "text",   "enabled": True,  "order": 6},
                {"key": "supplier",            "label": "Film Supplier",       "field_type": "text",   "enabled": True,  "order": 7},
                {"key": "rm_number",           "label": "R.M #",               "field_type": "text",   "enabled": False, "order": 8},
                {"key": "order_qty",           "label": "Order Qty",           "field_type": "number", "enabled": True,  "order": 9},
                {"key": "web_size",            "label": "Size (Inches)",       "field_type": "text",   "enabled": True,  "order": 10},
                {"key": "mic",                 "label": "MIC",                 "field_type": "text",   "enabled": True,  "order": 11},
                {"key": "cylinder_size",       "label": "Cylinder Size",       "field_type": "text",   "enabled": False, "order": 12},
                {"key": "no_of_colors",        "label": "No. of Colors",       "field_type": "number", "enabled": False, "order": 13},
                {"key": "ink_gsm",             "label": "Ink GSM",             "field_type": "number", "enabled": False, "order": 14},
                {"key": "speed",               "label": "Speed",               "field_type": "number", "enabled": False, "order": 15},
                {"key": "block_number",        "label": "Block #",             "field_type": "text",   "enabled": False, "order": 16},
                {"key": "tube_sheet",          "label": "Tube/Sheet",          "field_type": "text",   "enabled": True,  "order": 17},
                {"key": "bag_size",            "label": "Bag Size",            "field_type": "text",   "enabled": True,  "order": 18},
                {"key": "setting_time",        "label": "Setting Time",        "field_type": "text",   "enabled": True,  "order": 19},
                {"key": "start_time",          "label": "Start Time",          "field_type": "text",   "enabled": True,  "order": 20},
                {"key": "end_time",            "label": "End Time",            "field_type": "text",   "enabled": True,  "order": 21},
                {"key": "plain_roll_wt",       "label": "Plain G.wt",          "field_type": "number", "enabled": False, "order": 22},
                {"key": "plain_bal",           "label": "Plain Bal",           "field_type": "number", "enabled": False, "order": 23},
                {"key": "printed_roll_number", "label": "Printed Roll #",      "field_type": "text",   "enabled": False, "order": 24},
                {"key": "printed_reel_wt",     "label": "Printed Net Wt.",     "field_type": "number", "enabled": True,  "order": 25},
                {"key": "core_wt",             "label": "Core Wt. B",          "field_type": "number", "enabled": False, "order": 26},
                {"key": "counter_meter",       "label": "Counter / Meter",     "field_type": "text",   "enabled": False, "order": 27},
                {"key": "balance_rejected",    "label": "Balance / Rejected",  "field_type": "text",   "enabled": False, "order": 28},
                {"key": "gross_wt",            "label": "Printed G.wt",        "field_type": "number", "enabled": False, "order": 29},
                {"key": "net_wt",              "label": "Plain Net Wt.",        "field_type": "number", "enabled": True,  "order": 30},
                {"key": "total_counter",       "label": "Total Counter",       "field_type": "number", "enabled": False, "order": 31},
                {"key": "total_meter",         "label": "Total Meter",         "field_type": "number", "enabled": False, "order": 32},
                {"key": "setting_waste",       "label": "Setting Waste",       "field_type": "number", "enabled": False, "order": 33},
                {"key": "roll_waste",          "label": "Roll Waste",          "field_type": "number", "enabled": False, "order": 34},
                {"key": "printed_waste",       "label": "Printed Wastage",     "field_type": "number", "enabled": True,  "order": 35},
                {"key": "plain_waste",         "label": "Plain Wastage",       "field_type": "number", "enabled": True,  "order": 36},
                {"key": "total_waste",         "label": "Total Waste",         "field_type": "number", "enabled": False, "order": 37},
                {"key": "rejected_core_wt",    "label": "Rejected Core Wt.",   "field_type": "number", "enabled": False, "order": 38},
                {"key": "prepared_by",         "label": "Prepared By",         "field_type": "text",   "enabled": False, "order": 39},
                {"key": "supervisor",          "label": "Supervisor",          "field_type": "text",   "enabled": False, "order": 40},
                {"key": "remarks",             "label": "Remarks",             "field_type": "text",   "enabled": False, "order": 41},
            ],
        },
        {
            "code": "F-PRD/01.1",
            "name": "Gravure Printing Production Report",
            "keywords": ["gravure", "F-PRD/01.1", "gravure printing"],
            "fields": [
                {"key": "print_date",          "label": "Print Date",            "field_type": "date",   "enabled": True,  "order": 1},
                {"key": "job_name",            "label": "Job Name",              "field_type": "text",   "enabled": True,  "order": 2},
                {"key": "job_code",            "label": "Job Code",              "field_type": "text",   "enabled": True,  "order": 3},
                {"key": "plain_order_qty",     "label": "Plain Order Qty",       "field_type": "number", "enabled": True,  "order": 4},
                {"key": "material",            "label": "Material",              "field_type": "text",   "enabled": True,  "order": 5},
                {"key": "material_supplier",   "label": "Material Supplier",     "field_type": "text",   "enabled": True,  "order": 6},
                {"key": "web_size_mic",        "label": "Web Size & MIC",        "field_type": "text",   "enabled": True,  "order": 7},
                {"key": "cylinder_qty_number", "label": "Cylinder Qty & #",      "field_type": "text",   "enabled": True,  "order": 8},
                {"key": "cylinder_length_cir", "label": "Cylinder Length x Cir", "field_type": "text",   "enabled": True,  "order": 9},
                {"key": "speed",               "label": "Speed",                 "field_type": "number", "enabled": True,  "order": 10},
                {"key": "operator",            "label": "Operator",              "field_type": "text",   "enabled": True,  "order": 11},
                {"key": "color_man",           "label": "Color Man",             "field_type": "text",   "enabled": True,  "order": 12},
                {"key": "ink_gsm",             "label": "Ink GSM",               "field_type": "number", "enabled": True,  "order": 13},
                {"key": "setting_time",        "label": "Setting Time",          "field_type": "text",   "enabled": True,  "order": 14},
                {"key": "start_time",          "label": "Start Time",            "field_type": "text",   "enabled": True,  "order": 15},
                {"key": "end_time",            "label": "End Time",              "field_type": "text",   "enabled": True,  "order": 16},
                {"key": "plain_gross_wt",      "label": "Plain Gross Wt.",       "field_type": "number", "enabled": True,  "order": 17},
                {"key": "printed_gross_wt",    "label": "Printed Gross Wt.",     "field_type": "number", "enabled": True,  "order": 18},
                {"key": "plain_core_wt",       "label": "Plain Core Wt.",        "field_type": "number", "enabled": True,  "order": 19},
                {"key": "printed_core_wt",     "label": "Printed Core Wt.",      "field_type": "number", "enabled": True,  "order": 20},
                {"key": "plain_balance",       "label": "Plain Balance",         "field_type": "number", "enabled": True,  "order": 21},
                {"key": "plain_net_wt",        "label": "Plain Net Wt.",         "field_type": "number", "enabled": True,  "order": 22},
                {"key": "printed_net_wt",      "label": "Printed Net Wt.",       "field_type": "number", "enabled": True,  "order": 23},
                {"key": "total_mtr",           "label": "Total Mtr.",            "field_type": "number", "enabled": True,  "order": 24},
                {"key": "plain_waste",         "label": "Plain Waste",           "field_type": "number", "enabled": True,  "order": 25},
                {"key": "roll_waste",          "label": "Roll Waste",            "field_type": "number", "enabled": True,  "order": 26},
                {"key": "printed_waste",       "label": "Printed Waste",         "field_type": "number", "enabled": True,  "order": 27},
                {"key": "setting_waste",       "label": "Setting Waste",         "field_type": "number", "enabled": True,  "order": 28},
                {"key": "total_waste",         "label": "Total Waste",           "field_type": "number", "enabled": True,  "order": 29},
                {"key": "prepared_by",         "label": "Prepared By",           "field_type": "text",   "enabled": True,  "order": 30},
                {"key": "supervisor",          "label": "Supervisor",            "field_type": "text",   "enabled": True,  "order": 31},
                {"key": "remarks",             "label": "Remarks",               "field_type": "text",   "enabled": False, "order": 32},
            ],
        },
    ]

    for form_data in forms:
        existing = FormType.query.filter_by(code=form_data["code"]).first()
        if not existing:
            ft = FormType(
                code=form_data["code"],
                name=form_data["name"],
                keywords=",".join(form_data["keywords"]),
            )
            db.session.add(ft)
            db.session.flush()
            for f in form_data["fields"]:
                db.session.add(FieldConfig(
                    form_type_id=ft.id,
                    key=f["key"],
                    label=f["label"],
                    field_type=f["field_type"],
                    enabled=f["enabled"],
                    order=f["order"],
                ))
        else:
            existing_fields = {fc.key: fc for fc in existing.field_configs}
            for f in form_data["fields"]:
                if f["key"] in existing_fields:
                    fc = existing_fields[f["key"]]
                    fc.label = f["label"]
                    fc.enabled = f["enabled"]
                    fc.order = f["order"]
                else:
                    db.session.add(FieldConfig(
                        form_type_id=existing.id,
                        key=f["key"],
                        label=f["label"],
                        field_type=f["field_type"],
                        enabled=f["enabled"],
                        order=f["order"],
                    ))

    db.session.commit()