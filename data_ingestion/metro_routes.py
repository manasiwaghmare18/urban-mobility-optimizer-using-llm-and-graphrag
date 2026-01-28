import osmnx as ox
import pandas as pd
import os
from shapely.geometry import Point

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Hyderabad bounding box
HYDERABAD_BBOX = (
    17.60,  # north
    17.20,  # south
    78.70,  # east
    78.20   # west
)

# Metro-specific tags (OSM standard)
tags = {
    "railway": "station",
    "station": "subway"
}

print("Downloading Hyderabad Metro station data (production-safe)...")

gdf = ox.features_from_bbox(
    bbox=HYDERABAD_BBOX,
    tags=tags
)

def extract_lat_lon(geometry):
    if isinstance(geometry, Point):
        return geometry.y, geometry.x
    else:
        centroid = geometry.centroid
        return centroid.y, centroid.x

records = []

for _, row in gdf.iterrows():
    if row.geometry is None:
        continue

    lat, lon = extract_lat_lon(row.geometry)

    records.append({
        "name": row.get("name", "Unnamed Metro Station"),
        "lat": lat,
        "lon": lon
    })

df = pd.DataFrame(records).drop_duplicates()

output_path = os.path.join(DATA_DIR, "metro_stations.csv")
df.to_csv(output_path, index=False)

print(f"SUCCESS: {len(df)} metro stations saved to {output_path}")
