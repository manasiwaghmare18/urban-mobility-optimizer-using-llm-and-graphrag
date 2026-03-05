# data_ingestion/road_network.py

import os
import osmnx as ox
import networkx as nx
import pandas as pd
from typing import Dict, List

# Restrict data strictly to Hyderabad
HYDERABAD_PLACE = "Hyderabad, Telangana, India"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def fetch_hyderabad_road_network() -> nx.MultiDiGraph:
    """
    Fetch drivable road network for Hyderabad from OpenStreetMap.
    """
    print("Downloading Hyderabad road network from OpenStreetMap...")
    graph = ox.graph_from_place(
        HYDERABAD_PLACE,
        network_type="drive",
        simplify=True
    )
    print(f"Road network downloaded: {len(graph.nodes)} nodes, {len(graph.edges)} edges")
    return graph


def extract_nodes(graph: nx.MultiDiGraph) -> Dict[int, Dict]:
    """
    Extract intersection/junction nodes with geo-coordinates.
    """
    nodes = {}

    for node_id, data in graph.nodes(data=True):
        nodes[node_id] = {
            "latitude": data.get("y"),
            "longitude": data.get("x")
        }

    print(f"Extracted {len(nodes)} nodes")
    return nodes


def extract_road_segments(graph: nx.MultiDiGraph) -> List[Dict]:
    """
    Convert NetworkX edges into clean road segment records.
    """
    road_segments = []

    for u, v, key, data in graph.edges(keys=True, data=True):
        if "length" not in data:
            continue

        road_segments.append({
            "from_node": u,
            "to_node": v,
            "length_meters": data["length"],
            "road_type": str(data.get("highway", "unknown")),
            "oneway": bool(data.get("oneway", False))
        })

    print(f"Extracted {len(road_segments)} road segments")
    return road_segments


# ------------------------------------------------
# SAVE TO CSV
# ------------------------------------------------
def save_to_csv(nodes: Dict[int, Dict], road_segments: List[Dict]):
    nodes_df = pd.DataFrame([
        {
            "node_id": node_id,
            "latitude": data["latitude"],
            "longitude": data["longitude"]
        }
        for node_id, data in nodes.items()
    ])

    roads_df = pd.DataFrame(road_segments)

    nodes_path = os.path.join(DATA_DIR, "nodes.csv")
    roads_path = os.path.join(DATA_DIR, "road_segments.csv")

    nodes_df.to_csv(nodes_path, index=False)
    roads_df.to_csv(roads_path, index=False)

    print(f"✅ Nodes saved to {nodes_path}")
    print(f"✅ Road segments saved to {roads_path}")


# ------------------------------------------------
# MAIN (RUN THIS FILE DIRECTLY)
# ------------------------------------------------
if __name__ == "__main__":
    graph = fetch_hyderabad_road_network()
    nodes = extract_nodes(graph)
    road_segments = extract_road_segments(graph)

    save_to_csv(nodes, road_segments)

    print("🎯 Road network extraction + CSV export complete")
