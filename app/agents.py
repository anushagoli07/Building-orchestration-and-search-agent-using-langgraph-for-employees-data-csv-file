import json
import logging
from functools import lru_cache
from typing import Any

import pandas as pd
from google import genai
from google.genai import types
from langchain_core.messages import AIMessage

from .config import GEMINI_MODEL, TARGET_CSV
from .data import load_employee_data
from .models import AgentFilters, AgentState

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_gemini_client() -> genai.Client:
    return genai.Client()


def orchestration_agent(state: AgentState) -> dict[str, Any]:
    messages = state.get("messages", [])
    if not messages:
        return {"error": "No user query was provided."}

    user_query = str(messages[-1].content)
    prompt = f"""
Analyze this payroll query and map all constraints into the following JSON schema:
- countries: List of strings
- years: List of integers
- designations: List of strings
- salary_above_inr: Integer annual INR threshold when relevant
- salary_above_usd: Integer monthly threshold when relevant

User query: {user_query}
"""

    try:
        response = get_gemini_client().models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=AgentFilters,
                temperature=0.1,
            ),
        )
        if not response.text:
            raise ValueError("Gemini returned an empty filter response")
        extracted_filters = json.loads(response.text)
        extracted_filters = {
            key: value for key, value in extracted_filters.items() if value is not None
        }
        return {
            "search_filters": extracted_filters,
            "messages": [AIMessage(
                content=f"[Orchestrator]: Query parsed successfully. Target parameters: {extracted_filters}"
            )],
        }
    except Exception as error:
        logger.exception("Could not parse payroll query")
        message = f"[Orchestrator Error]: {error}"
        return {"error": message, "messages": [AIMessage(content=message)]}


def search_agent(state: AgentState) -> dict[str, Any]:
    error = state.get("error")
    if error:
        return {"messages": [AIMessage(content=error)]}

    filters = state.get("search_filters", {})
    try:
        dataframe = load_employee_data(TARGET_CSV)
        dataframe["monthly_salary"] = (dataframe["annual_salary"] / 12).round(2)
        dataframe["monthly_tax"] = (dataframe["annual_tax"] / 12).round(2)

        years = filters.get("years")
        if years:
            dataframe = dataframe[dataframe["year"].isin(years)]
        designations = filters.get("designations")
        if designations:
            roles = [role.lower() for role in designations]
            dataframe = dataframe[dataframe["designation"].str.lower().isin(roles)]
        countries_filter = filters.get("countries")
        if countries_filter:
            countries = [country.lower() for country in countries_filter]
            dataframe = dataframe[dataframe["country"].str.lower().isin(countries)]
        salary_above_inr = filters.get("salary_above_inr")
        if salary_above_inr is not None:
            dataframe = dataframe[
                (dataframe["country"].str.lower() != "india")
                | (dataframe["annual_salary"] >= salary_above_inr)
            ]
        salary_above_usd = filters.get("salary_above_usd")
        if salary_above_usd is not None:
            dataframe = dataframe[dataframe["monthly_salary"] >= salary_above_usd]

        report_columns = [
            "emp_id", "name", "country", "state", "designation", "year",
            "annual_salary", "monthly_salary", "annual_tax", "monthly_tax",
        ]
        result = dataframe[report_columns].sort_values(
            by=["country", "annual_salary"], ascending=False
        )
        table = result.to_string(index=False, justify="left")
        return {"messages": [AIMessage(
            content=(
                f"[Search Agent]: Found {len(result)} matching employee-year records "
                f"across the payroll data:\n\n{table}"
            )
        )]}
    except Exception as error:
        logger.exception("Could not search employee data")
        message = f"[Search Agent Error]: {error}"
        return {"error": message, "messages": [AIMessage(content=message)]}
