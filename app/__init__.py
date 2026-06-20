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
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }
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
                {"key": "web_size",            "label": "Web Size",            "field_type": "text",   "enabled": True,  "order": 10},
                {"key": "mic",                 "label": "MIC",                 "field_type": "text",   "enabled": True,  "order": 11},
                {"key": "cylinder_size",       "label": "Cylinder Size",       "field_type": "text",   "enabled": False, "order": 12},
                {"key": "no_of_colors",        "label": "No. of Colors",       "field_type": "number", "enabled": False, "order": 13},
                {"key": "ink_gsm",             "label": "Ink GSM",             "field_type": "number", "enabled": False, "order": 14},
                {"key": "speed",               "label": "Speed",               "field_type": "number", "enabled": False, "order": 15},
                {"key": "block_number",        "label": "Block #",             "field_type": "text",   "enabled": False, "order": 16},
                {"key": "tube_sheet",          "label": "Tube/Sheet",          "field_type": "select", "options": '["Tube","Sheet"]', "enabled": True,  "order": 17},
                {"key": "bag_size",            "label": "Bag Size",            "field_type": "text",   "enabled": True,  "order": 18},
                {"key": "setting_time",        "label": "Setting Time",        "field_type": "text",   "enabled": True,  "order": 19},
                {"key": "start_time",          "label": "Start Time",          "field_type": "text",   "enabled": True,  "order": 20},
                {"key": "end_time",            "label": "End Time",            "field_type": "text",   "enabled": True,  "order": 21},
                {"key": "plain_roll_wt",       "label": "Plain G.wt",          "field_type": "number", "enabled": False, "order": 22},
                {"key": "plain_bal",           "label": "Plain Bal",           "field_type": "number", "enabled": False, "order": 23},
                {"key": "printed_roll_number", "label": "Printed Roll #",      "field_type": "text",   "enabled": False, "order": 24},
                {"key": "printed_reel_wt",     "label": "Printed Net Wt.",     "field_type": "number", "enabled": True,  "order": 30},
                {"key": "core_wt",             "label": "Core Wt. B",          "field_type": "number", "enabled": False, "order": 26},
                {"key": "counter_meter",       "label": "Counter / Meter",     "field_type": "text",   "enabled": False, "order": 27},
                {"key": "balance_rejected",    "label": "Balance / Rejected",  "field_type": "text",   "enabled": False, "order": 28},
                {"key": "gross_wt",            "label": "Printed G.wt",        "field_type": "number", "enabled": False, "order": 29},
                {"key": "net_wt",              "label": "Plain Net Wt.",        "field_type": "number", "enabled": True,  "order": 25},
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
        {
            "code": "F-PRD/02.1",
            "name": "Lamination Production Report",
            "keywords": ["lamination", "F-PRD/02.1", "lamination production"],
            "fields": [
                {"key": "job_code",                "label": "Job Code",                     "field_type": "text",   "enabled": True,  "order": 1},
                {"key": "stage_code",              "label": "Stage Code",                   "field_type": "text",   "enabled": True,  "order": 2},
                {"key": "month",                   "label": "Month",                        "field_type": "text",   "enabled": True,  "order": 3},
                {"key": "date",                    "label": "Date",                         "field_type": "date",   "enabled": True,  "order": 4},
                {"key": "job_name",                "label": "Job Name",                     "field_type": "text",   "enabled": True,  "order": 5},
                {"key": "machine",                 "label": "Machine",                      "field_type": "text",   "enabled": True,  "order": 6},
                {"key": "shift",                   "label": "Shift",                        "field_type": "text",   "enabled": True,  "order": 7},
                {"key": "speed",                   "label": "Speed",                        "field_type": "number", "enabled": True,  "order": 8},
                {"key": "start_time",              "label": "Start Time",                   "field_type": "text",   "enabled": True,  "order": 9},
                {"key": "end_time",                "label": "End Time",                     "field_type": "text",   "enabled": True,  "order": 10},
                {"key": "structure",               "label": "Structure",                    "field_type": "text",   "enabled": True,  "order": 11},
                {"key": "film_a",                  "label": "Film A",                       "field_type": "text",   "enabled": True,  "order": 12},
                {"key": "film_a_size_micron",      "label": "Film A Size / Micron",         "field_type": "text",   "enabled": True,  "order": 13},
                {"key": "film_b",                  "label": "Film B",                       "field_type": "text",   "enabled": True,  "order": 14},
                {"key": "film_b_size_micron",      "label": "Film B Size / Micron",         "field_type": "text",   "enabled": True,  "order": 15},
                {"key": "glue_coating_size",       "label": "Glue Coating Size",            "field_type": "text",   "enabled": True,  "order": 16},
                {"key": "total_printed_film_qty",  "label": "Total Printed Film Qty",       "field_type": "number", "enabled": True,  "order": 17},
                {"key": "printed_wastage",         "label": "Printed Wastage",              "field_type": "number", "enabled": True,  "order": 18},
                {"key": "total_film_b_qty",        "label": "Total Film B Qty",             "field_type": "number", "enabled": True,  "order": 19},
                {"key": "film_b_wastage",          "label": "Film B Wastage",               "field_type": "number", "enabled": True,  "order": 20},
                {"key": "total_order_qty",         "label": "Total Order Quantity",         "field_type": "number", "enabled": True,  "order": 21},
                {"key": "total_laminated_qty",     "label": "Total Laminated Qty",          "field_type": "number", "enabled": True,  "order": 22},
                {"key": "job_status",              "label": "Job Status",                   "field_type": "text",   "enabled": True,  "order": 23},
                {"key": "total_laminated_meters",  "label": "Total Laminated Meters",       "field_type": "number", "enabled": True,  "order": 24},
                {"key": "laminated_wastage",       "label": "Laminated Wastage",            "field_type": "number", "enabled": True,  "order": 25},
                {"key": "glue_ratio",              "label": "Glue Ratio",                   "field_type": "text",   "enabled": True,  "order": 26},
                {"key": "glue_type",               "label": "Glue Type",                    "field_type": "select", "options": '["Solvent-based","Solvent less"]', "enabled": True,  "order": 27},
                {"key": "hardner",                 "label": "Hardner",                      "field_type": "number", "enabled": True,  "order": 28},
                {"key": "resin",                   "label": "Resin",                        "field_type": "number", "enabled": True,  "order": 29},
                {"key": "glue_consumption_no_solvent", "label": "Glue Consumption (No Solvent)", "field_type": "number", "enabled": False, "order": 30},
                {"key": "a_component_resin",       "label": "A-Component Resin",            "field_type": "number", "enabled": False, "order": 31},
                {"key": "b_component_hardner",     "label": "B-Component Hardner",          "field_type": "number", "enabled": False, "order": 32},
                {"key": "ethyl_acetate",           "label": "Ethyl Acetate",                "field_type": "number", "enabled": False, "order": 33},
                {"key": "total_batch_qty",         "label": "Total Batch Qty",              "field_type": "number", "enabled": False, "order": 34},
                {"key": "a_resin_consumption",     "label": "A-Component Resin Consumption","field_type": "number", "enabled": False, "order": 35},
                {"key": "b_hardner_consumption",   "label": "B-Component Hardner Consumption","field_type":"number","enabled": False, "order": 36},
                {"key": "ea_consumption",          "label": "Ethyl Acetate Consumption",    "field_type": "number", "enabled": False, "order": 37},
                {"key": "a_resin_rate",            "label": "A-Component Resin Rate",       "field_type": "number", "enabled": False, "order": 38},
                {"key": "b_hardner_rate",          "label": "B-Component Hardner Rate",     "field_type": "number", "enabled": False, "order": 39},
                {"key": "ea_rate",                 "label": "Rate of Ethyl Acetate",        "field_type": "number", "enabled": False, "order": 40},
                {"key": "a_cost",                  "label": "Component A Cost",             "field_type": "number", "enabled": False, "order": 41},
                {"key": "b_cost",                  "label": "Component B Cost",             "field_type": "number", "enabled": False, "order": 42},
                {"key": "c_cost",                  "label": "Component C Cost",             "field_type": "number", "enabled": False, "order": 43},
                {"key": "total_cost",              "label": "Total Cost",                   "field_type": "number", "enabled": False, "order": 44},
                {"key": "glue_cost_per_kg",        "label": "Glue Cost Per KG",             "field_type": "number", "enabled": False, "order": 45},
                {"key": "remarks",                 "label": "Remarks",                      "field_type": "text",   "enabled": False, "order": 46},
            ],
        },
        {
            "code": "F-PRD/03.1",
            "name": "Slitting Production Report",
            "keywords": ["slitting", "F-PRD/03.1", "slitting production"],
            "fields": [
                {"key": "job_code",               "label": "Job Code",               "field_type": "text",   "enabled": True,  "order": 1},
                {"key": "date",                   "label": "Date",                   "field_type": "date",   "enabled": True,  "order": 2},
                {"key": "job_name",               "label": "Job Name",               "field_type": "text",   "enabled": True,  "order": 3},
                {"key": "structure",              "label": "Structure",              "field_type": "text",   "enabled": True,  "order": 4},
                {"key": "overall_mic",            "label": "Overall MIC (µ)",        "field_type": "text",   "enabled": True,  "order": 5},
                {"key": "slitting_size",          "label": "Slitting Size",          "field_type": "text",   "enabled": True,  "order": 6},
                {"key": "outter_dia",             "label": "Outter Dia",             "field_type": "text",   "enabled": True,  "order": 7},
                {"key": "inner_dia",              "label": "Inner Dia",              "field_type": "text",   "enabled": True,  "order": 8},
                {"key": "start_time",             "label": "Start Time",             "field_type": "text",   "enabled": True,  "order": 9},
                {"key": "end_time",               "label": "End Time",               "field_type": "text",   "enabled": True,  "order": 10},
                {"key": "operator",               "label": "Operator",               "field_type": "text",   "enabled": True,  "order": 11},
                {"key": "shift",                  "label": "Shift",                  "field_type": "text",   "enabled": True,  "order": 12},
                {"key": "total_mother_reels",     "label": "Total Mother Reels",     "field_type": "number", "enabled": True,  "order": 13},
                {"key": "total_slitted_reels",    "label": "Total Slitted Reels",    "field_type": "number", "enabled": True,  "order": 14},
                {"key": "single_slitted_reel_wt", "label": "Single Slitted Reel Wt.","field_type": "number", "enabled": True,  "order": 15},
                {"key": "slitted_reel_wt",        "label": "Slitted Reel Wt.",       "field_type": "number", "enabled": True,  "order": 16},
                {"key": "mother_reel_wt",         "label": "Mother Reel Wt",         "field_type": "number", "enabled": True,  "order": 17},
                {"key": "setting_wastage",        "label": "Setting Wastage",        "field_type": "number", "enabled": True,  "order": 18},
                {"key": "trim_waste",             "label": "Trim Waste",             "field_type": "number", "enabled": True,  "order": 19},
                {"key": "trim_size",              "label": "Trim Size",              "field_type": "text",   "enabled": True,  "order": 20},
                {"key": "remarks",                "label": "Remarks",                "field_type": "text",   "enabled": False, "order": 21},
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
                    options=f.get("options"),
                    enabled=f["enabled"],
                    order=f["order"],
                ))
        else:
            existing_fields = {fc.key: fc for fc in existing.field_configs}
            for f in form_data["fields"]:
                if f["key"] in existing_fields:
                    fc = existing_fields[f["key"]]
                    fc.label = f["label"]
                    fc.field_type = f["field_type"]
                    fc.options = f.get("options")
                    fc.enabled = f["enabled"]
                    fc.order = f["order"]
                else:
                    db.session.add(FieldConfig(
                        form_type_id=existing.id,
                        key=f["key"],
                        label=f["label"],
                        field_type=f["field_type"],
                        options=f.get("options"),
                        enabled=f["enabled"],
                        order=f["order"],
                    ))

    db.session.commit()