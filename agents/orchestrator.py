from agents.planner_agent import PlannerAgent
from agents.route_agent import RouteAgent
from agents.weather_agent import WeatherAgent
from agents.cost_agent import CostAgent
from agents.transport_agent import TransportAgent
from agents.graph_rag_agent import GraphRAGAgent
from llm.llm_client import generate_explanation


class OrchestratorAgent:
    def __init__(self, conn):
        self.conn = conn

        self.planner = PlannerAgent()
        self.route_agent = RouteAgent(conn)
        self.weather_agent = WeatherAgent()
        self.cost_agent = CostAgent()
        self.transport_agent = TransportAgent(conn)
        self.graph_rag_agent = GraphRAGAgent(conn)

    def handle_request(self, source, destination):
        src_lat, src_lon = source
        dst_lat, dst_lon = destination

        plan = self.planner.create_plan("optimize urban travel")
        context = {}

        # 1️⃣ Route
        if "route" in plan:
            route = self.route_agent.find_route(src_lat, src_lon, dst_lat, dst_lon)
            if not route:
                return {"error": "No route found"}
            context["distance_km"] = round(route["distance_m"] / 1000, 2)

        # 2️⃣ Weather
        if "weather" in plan:
            context["weather"] = self.weather_agent.analyze(
                (src_lat + dst_lat) / 2,
                (src_lon + dst_lon) / 2
            )

        # 3️⃣ Cost & time
        if "cost" in plan:
            context["cost"] = self.cost_agent.estimate(route["distance_m"])

        # 4️⃣ Transport
        if "transport" in plan:
            context["transport"] = self.transport_agent.check_availability(
                src_lat, src_lon, dst_lat, dst_lon
            )

            if not context["transport"]["bus_available"]:
                context["cost"]["bus_cost_rs"] = "N/A"
                context["cost"]["bus_time_min"] = "N/A"

            if not context["transport"]["metro_available"]:
                context["cost"]["metro_cost_rs"] = "N/A"
                context["cost"]["metro_time_min"] = "N/A"

        # 5️⃣ GraphRAG
        if "graph_context" in plan:
            context["graph_context"] = self.graph_rag_agent.fetch_context(
                src_lat, src_lon, dst_lat, dst_lon
            )

        # 6️⃣ LLM Explanation
        explanation = generate_explanation(
            route={"distance_km": context["distance_km"]},
            weather=context["weather"],
            cost=context["cost"],
            transport=context["transport"]
        )

        context["llm_explanation"] = explanation
        context["route_method"] = "graph"

        return context
