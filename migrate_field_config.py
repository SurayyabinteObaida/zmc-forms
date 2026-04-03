"""
migrate_field_config.py
Run once to fix Flexo field labels and enabled states to match current form.
Usage: python migrate_field_config.py  (from project root)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from app import db
from app.models import FormType


def run():
    flexo = FormType.query.filter_by(code="F-PRD/01.2").first()
    if not flexo:
        print("ERROR: Flexo form type not found.")
        return

    label_fixes = {
        "date":             "Print Date",
        "net_wt":           "Plain Net Wt.",
        "printed_reel_wt":  "Printed Net Wt.",
        "plain_roll_wt":    "Plain G.wt",
        "gross_wt":         "Printed G.wt",
        "core_wt":          "Core Wt. B",
        "plain_bal":        "Plain Bal",
        "web_size":         "Size (Inches)",
        "material":         "Printed Film",
        "supplier":         "Film Supplier",
    }

    enabled_keys = {
        "date", "job_code", "job_name", "bag_size", "material",
        "tube_sheet", "web_size", "supplier", "order_qty",
        "net_wt", "printed_reel_wt", "printed_waste", "plain_waste",
        "operator", "setting_time", "start_time", "end_time", "mic",
    }

    updated = 0
    for fc in flexo.field_configs:
        changed = False

        if fc.key in label_fixes:
            fc.label = label_fixes[fc.key]
            changed = True

        should_be_enabled = fc.key in enabled_keys
        if fc.enabled != should_be_enabled:
            fc.enabled = should_be_enabled
            changed = True

        if changed:
            updated += 1

    db.session.commit()
    print(f"Done. {updated} field configs updated.")


with app.app_context():
    run()