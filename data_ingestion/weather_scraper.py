import requests
import time
from typing import Dict, List
from math import radians, cos, sin, sqrt, atan2

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geo points in km.
    """
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


# ------------------------------------------------
# REAL-TIME WEATHER FETCH (RATE-LIMITED + RETRY)
# ------------------------------------------------
def fetch_realtime_weather(lat: float, lon: float, retries: int = 3) -> Dict:
    """
    Fetch real-time weather using Open-Meteo (FREE, no API key).
    Includes retry & rate limiting to avoid SSL/API errors.
    """
    url = (
        f"{OPEN_METEO_URL}"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "current_weather" not in data:
                return None

            current = data["current_weather"]

            return {
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed"),
                "weathercode": current.get("weathercode"),
                "timestamp": current.get("time")
            }

        except Exception as e:
            print(f"Weather retry {attempt + 1}/{retries} failed:", e)
            time.sleep(1)  # ⭐ backoff before retry

    return None


# ------------------------------------------------
# ENRICH ROAD SEGMENTS WITH REAL-TIME WEATHER
# ------------------------------------------------
def enrich_roads_with_weather(
    road_segments: List[Dict],
    nodes: Dict[int, Dict]
) -> List[Dict]:
    """
    Attach real-time weather to road segments.
    Weather is fetched using midpoint of road segment.
    """
    enriched_segments = []

    for segment in road_segments:
        from_node = nodes.get(segment["from_node"])
        to_node = nodes.get(segment["to_node"])

        if not from_node or not to_node:
            continue

        # Mid-point of road segment
        mid_lat = (from_node["latitude"] + to_node["latitude"]) / 2
        mid_lon = (from_node["longitude"] + to_node["longitude"]) / 2

        weather = fetch_realtime_weather(mid_lat, mid_lon)

        segment["weather"] = weather
        enriched_segments.append(segment)

        # ⭐ RATE LIMIT (VERY IMPORTANT)
        time.sleep(0.3)

    print(f"Weather mapped to {len(enriched_segments)} road segments")
    return enriched_segments
