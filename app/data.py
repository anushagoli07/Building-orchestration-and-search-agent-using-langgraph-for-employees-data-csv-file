import random
from pathlib import Path

import pandas as pd


COUNTRIES = [
    "Australia", "India", "Canada", "USA", "UK", "Germany", "France",
    "Japan", "Brazil", "South Africa",
]
STATES = {
    "Australia": ["New South Wales", "Victoria", "Queensland"],
    "India": ["Maharashtra", "Delhi", "Karnataka"],
    "Canada": ["Ontario", "British Columbia", "Quebec"],
    "USA": ["California", "Texas", "New York"],
    "UK": ["England", "Scotland", "Wales"],
    "Germany": ["Bavaria", "Berlin", "Hamburg"],
    "France": ["Île-de-France", "Provence", "Auvergne-Rhône-Alpes"],
    "Japan": ["Tokyo", "Osaka", "Kyoto"],
    "Brazil": ["São Paulo", "Rio de Janeiro", "Minas Gerais"],
    "South Africa": ["Gauteng", "Western Cape", "KwaZulu-Natal"],
}
DESIGNATIONS = ["Engineer", "Manager", "Analyst", "Director", "Specialist"]
NAMES = [
    "Sam", "Leo", "Mia", "Max", "Ava", "Ben", "Zoe", "Ian", "Eva", "Jon",
    "Ali", "Jay", "Joy", "Roy", "Amy", "Dan", "Fay", "Ned", "Kai", "Tim",
    "Bob", "Tom", "Jim", "Joe", "Ted", "Ann", "Sue", "Kim", "Jan", "Ron",
    "Ken", "Don", "Ray", "Guy", "Rex", "Uma", "Ivy", "Ada", "Lee", "Mac",
    "Gus", "Lou", "Art", "Hal", "Val", "Cal", "Sal", "Abe",
]


def generate_employee_csv(target_path: Path) -> None:
    random.seed(42)
    data = []
    employee_number = 1

    for country in COUNTRIES:
        for _ in range(10):
            employee_id = f"EMP{employee_number:03d}"
            name = NAMES[(employee_number - 1) % len(NAMES)]
            state = random.choice(STATES[country])
            designation = random.choice(DESIGNATIONS)

            if country == "India":
                base_salary = random.randint(600000, 2400000)
            elif country == "Japan":
                base_salary = random.randint(4500000, 11000000)
            else:
                base_salary = random.randint(45000, 140000)

            tax_rate = random.uniform(0.15, 0.35)
            for year in (2025, 2026):
                annual_salary = int(
                    base_salary if year == 2025 else base_salary * random.uniform(1.03, 1.07)
                )
                data.append({
                    "emp_id": employee_id,
                    "name": name,
                    "country": country,
                    "state": state,
                    "designation": designation,
                    "year": year,
                    "annual_salary": annual_salary,
                    "annual_tax": int(annual_salary * tax_rate),
                })
            employee_number += 1

    target_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(data).to_csv(target_path, index=False)


def load_employee_data(target_path: Path) -> pd.DataFrame:
    if not target_path.exists():
        raise FileNotFoundError(
            f"Employee data was not found at {target_path}. "
            "Run generate_csv.py first."
        )
    return pd.read_csv(target_path)
