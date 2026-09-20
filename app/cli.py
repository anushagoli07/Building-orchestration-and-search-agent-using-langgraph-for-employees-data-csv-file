from langchain_core.messages import AIMessage, HumanMessage

from .graph import build_graph


def run_cli() -> None:
    graph = build_graph()
    print("=" * 70)
    print("Fully Autonomous Financial Auditor Agent Online!")
    print("=" * 70)

    while True:
        try:
            user_prompt = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_prompt.lower() in {"exit", "quit"}:
            break
        if not user_prompt:
            continue

        outputs = graph.invoke({
            "messages": [HumanMessage(content=user_prompt)],
            "search_filters": {},
        })
        for message in outputs.get("messages", []):
            if isinstance(message, AIMessage):
                print(f"\n{message.content}\n" + "-" * 50)
