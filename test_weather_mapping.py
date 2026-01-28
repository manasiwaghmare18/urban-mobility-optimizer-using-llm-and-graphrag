# test_weather_mapping.py

from data_ingestion.road_network import (
    fetch_hyderabad_road_network,
    extract_nodes,
    extract_road_segments
)
from data_ingestion.weather_scraper import enrich_roads_with_weather

graph = fetch_hyderabad_road_network()
nodes = extract_nodes(graph)
roads = extract_road_segments(graph)

# Test on small subset (important!)
sample_roads = roads[:20]

enriched = enrich_roads_with_weather(sample_roads, nodes)

print(enriched[0])
