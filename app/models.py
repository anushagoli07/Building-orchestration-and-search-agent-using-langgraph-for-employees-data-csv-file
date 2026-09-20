from typing import Annotated, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class AgentFilters(TypedDict, total=False):
    countries: Optional[List[str]]
    years: Optional[List[int]]
    designations: Optional[List[str]]
    salary_above_inr: Optional[int]
    salary_above_usd: Optional[int]


class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage], add_messages]
    search_filters: AgentFilters
    error: Optional[str]
