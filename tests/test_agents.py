import unittest
from unittest.mock import patch

from langchain_core.messages import HumanMessage

from app.agents import search_agent
from app.models import AgentState


class SearchAgentTests(unittest.TestCase):
    def setUp(self):
        self.state: AgentState = {
            "messages": [HumanMessage(content="test")],
            "search_filters": {},
        }

    def test_applies_country_and_indian_salary_filters(self):
        self.state["search_filters"] = {
            "countries": ["India"],
            "salary_above_inr": 2_000_000,
        }

        result = search_agent(self.state)
        content = result["messages"][0].content

        self.assertNotIn("Canada", content)
        self.assertNotIn("1973875", content)
        self.assertIn("India", content)

    def test_searches_all_employee_year_records_with_payroll_fields(self):
        result = search_agent(self.state)
        content = result["messages"][0].content

        self.assertIn("Found 200 matching", content)
        for column in ("emp_id", "state", "annual_salary", "monthly_salary", "annual_tax", "monthly_tax"):
            self.assertIn(column, content)

    @patch("app.agents.load_employee_data", side_effect=FileNotFoundError("missing data"))
    def test_reports_missing_data(self, _load_data):
        with self.assertLogs("app.agents", level="ERROR"):
            result = search_agent(self.state)

        self.assertIn("Search Agent Error", result["error"])
        self.assertIn("Search Agent Error", result["messages"][0].content)


if __name__ == "__main__":
    unittest.main()
