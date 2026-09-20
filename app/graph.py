from langgraph.graph import END, START, StateGraph

from .agents import orchestration_agent, search_agent
from .models import AgentState


def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("orchestration_agent", orchestration_agent)
    builder.add_node("search_agent", search_agent)
    builder.add_edge(START, "orchestration_agent")
    builder.add_edge("orchestration_agent", "search_agent")
    builder.add_edge("search_agent", END)
    return builder.compile()
