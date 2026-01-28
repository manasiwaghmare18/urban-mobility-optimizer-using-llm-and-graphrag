import pandas as pd

from graph_db.load_data import GraphLoader
from data_ingestion.weather_scraper import enrich_roads_with_weather

print("Starting full graph load...")

# ------------------------------------------------
# 1️⃣ LOAD ROAD DATA FROM CSV
# ------------------------------------------------
nodes_df = pd.read_csv("data/nodes.csv")
roads_df = pd.read_csv("data/road_segments.csv")

# Convert to expected formats
nodes = {
    int(row["node_id"]): {
        "latitude": row["latitude"],
        "longitude": row["longitude"]
    }
    for _, row in nodes_df.iterrows()
}

roads = roads_df.to_dict(orient="records")

loader = GraphLoader()
loader.load_locations_and_roads(nodes, roads)

# ------------------------------------------------
# 2️⃣ REAL-TIME WEATHER (LIMITED)
# ------------------------------------------------
WEATHER_ROAD_LIMIT = 500
roads_sample = roads[:WEATHER_ROAD_LIMIT]

roads_with_weather = enrich_roads_with_weather(
    road_segments=roads_sample,
    nodes=nodes
)

loader.load_weather(roads_with_weather)

# ------------------------------------------------
# 3️⃣ BUS STOPS
# ------------------------------------------------
bus_df = pd.read_csv("data/bus_stops.csv")
loader.load_bus_stops(bus_df.to_dict(orient="records"))

# ------------------------------------------------
# 4️⃣ METRO STATIONS
# ------------------------------------------------
metro_df = pd.read_csv("data/metro_stations.csv")
loader.load_metro_stations(metro_df.to_dict(orient="records"))

loader.close()

print("✅ Graph load complete (CSV → Neo4j)")
