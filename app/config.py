from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_CSV = PROJECT_ROOT / "employee_data.csv"
GEMINI_MODEL = "gemini-2.5-flash"
