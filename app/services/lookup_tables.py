"""
Master Lookup Tables from FLEXO_PRINTING_MASTER.xlsx
1,039 job names | 25 printed films | 15 suppliers
"""

# Import directly from the JSON file we already created
import json
import os

# Load lookup tables from JSON
_json_path = os.path.join(os.path.dirname(__file__), 'lookup_tables_from_excel.json')
with open(_json_path, 'r', encoding='utf-8') as f:
    LOOKUP_TABLES = json.load(f)
