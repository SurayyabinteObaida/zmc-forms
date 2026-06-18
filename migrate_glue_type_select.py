"""
migrate_glue_type_select.py
Adds the `options` column to field_configs and sets glue_type to a select field.
Run once from the project root: python migrate_glue_type_select.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import app
from app import db
from app.models import FormType


def run():
    # 1. Add column if it doesn't exist (PostgreSQL)
    with db.engine.connect() as conn:
        conn.execute(db.text(
            "ALTER TABLE field_configs ADD COLUMN IF NOT EXISTS options TEXT"
        ))
        conn.commit()
        print("Column 'options' ensured on field_configs.")

    # 2. Patch existing glue_type record for lamination
    lam = FormType.query.filter_by(code="F-PRD/02.1").first()
    if not lam:
        print("ERROR: Lamination form type (F-PRD/02.1) not found.")
        return

    for fc in lam.field_configs:
        if fc.key == "glue_type":
            fc.field_type = "select"
            fc.options = '["Solvent-based","Solvent less"]'
            print("glue_type updated → field_type=select, options=[Solvent-based, Solvent less]")
            break
    else:
        print("WARNING: glue_type field config not found.")

    db.session.commit()
    print("Done.")


with app.app_context():
    run()
