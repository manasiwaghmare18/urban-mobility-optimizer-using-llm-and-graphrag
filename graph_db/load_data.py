from graph_db.neo4j_connection import Neo4jConnection
from graph_db.graph_schema import create_constraints


class GraphLoader:
    def __init__(self):
        self.conn = Neo4jConnection()
        create_constraints(self.conn)

    # ------------------------------------------------
    # LOAD ROAD NETWORK (LOCATIONS + CONNECTS EDGES)
    # ------------------------------------------------
    def load_locations_and_roads(self, nodes, road_segments):
        print("Loading road locations and road segments...")

        # 1️⃣ Location nodes
        for node_id, node in nodes.items():
            self.conn.execute(
                """
                MERGE (l:Location {id: $id})
                SET l.lat = $lat,
                    l.lon = $lon
                """,
                {
                    "id": str(node_id),
                    "lat": float(node["latitude"]),
                    "lon": float(node["longitude"])
                }
            )

        # 2️⃣ CONNECTS relationships
        for road in road_segments:
            self.conn.execute(
                """
                MATCH (a:Location {id: $from_id}),
                      (b:Location {id: $to_id})
                MERGE (a)-[c:CONNECTS]->(b)
                SET c.length = $length,
                    c.road_type = $type
                """,
                {
                    "from_id": str(road["from_node"]),
                    "to_id": str(road["to_node"]),
                    "length": float(road["length_meters"]),
                    "type": str(road["road_type"])
                }
            )

        print("Road network loaded.")

    # ------------------------------------------------
    # LOAD / UPDATE REAL-TIME WEATHER (LOCATION → WEATHER)
    # ------------------------------------------------
    def load_weather(self, road_segments_with_weather):
        print("Loading real-time weather data...")

        for road in road_segments_with_weather:
            weather = road.get("weather")
            if not weather:
                continue

            self.conn.execute(
                """
                MATCH (l:Location {id: $location_id})
                MERGE (w:Weather {location_id: $location_id})
                SET w.temperature = $temp,
                    w.windspeed = $wind,
                    w.weather_code = $code,
                    w.updated_at = datetime($updated_at)
                MERGE (l)-[:HAS_WEATHER]->(w)
                """,
                {
                    "location_id": str(road["from_node"]),
                    "temp": float(weather["temperature"]),
                    "wind": float(weather["windspeed"]),
                    "code": int(weather["weathercode"]),
                    "updated_at": weather.get("timestamp")
                }
            )

        print("Weather data loaded / updated.")

    # ------------------------------------------------
    # LOAD BUS STOPS
    # ------------------------------------------------
    def load_bus_stops(self, bus_stops):
        print("Loading bus stops...")

        for i, stop in enumerate(bus_stops):
            lat = stop.get("lat") or stop.get("latitude")
            lon = stop.get("lon") or stop.get("longitude")
            if lat is None or lon is None:
                continue

            self.conn.execute(
                """
                MERGE (b:BusStop {id: $id})
                SET b.name = $name,
                    b.lat = $lat,
                    b.lon = $lon
                """,
                {
                    "id": f"bus_{i}",
                    "name": stop.get("name", "Unnamed Bus Stop"),
                    "lat": float(lat),
                    "lon": float(lon)
                }
            )

        print("Bus stops loaded.")

    # ------------------------------------------------
    # LOAD METRO STATIONS
    # ------------------------------------------------
    def load_metro_stations(self, stations):
        print("Loading metro stations...")

        for i, station in enumerate(stations):
            lat = station.get("lat") or station.get("latitude")
            lon = station.get("lon") or station.get("longitude")
            if lat is None or lon is None:
                continue

            self.conn.execute(
                """
                MERGE (m:MetroStation {id: $id})
                SET m.name = $name,
                    m.lat = $lat,
                    m.lon = $lon
                """,
                {
                    "id": f"metro_{i}",
                    "name": station.get("name", "Unnamed Metro Station"),
                    "lat": float(lat),
                    "lon": float(lon)
                }
            )

        print("Metro stations loaded.")

    # ------------------------------------------------
    # CLOSE CONNECTION
    # ------------------------------------------------
    def close(self):
        self.conn.close()
        print("Neo4j connection closed.")
