class PlannerAgent:
    """
    Decides what steps to execute dynamically.
    This is the core of agentic behavior.
    """

    def create_plan(self, user_goal: str):
        # Can later be LLM-driven
        return [
            "route",
            "weather",
            "cost",
            "transport",
            "graph_context",
            "explanation"
        ]
