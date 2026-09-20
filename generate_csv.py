from app.config import TARGET_CSV
from app.data import generate_employee_csv


if __name__ == "__main__":
    generate_employee_csv(TARGET_CSV)
    print(f"Generated employee data at {TARGET_CSV}")
