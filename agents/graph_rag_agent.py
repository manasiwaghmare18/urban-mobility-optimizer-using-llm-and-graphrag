class GraphRAGAgent:
    def __init__(self, conn):
        self.conn = conn

    def fetch_context(self, src_lat, src_lon, dst_lat, dst_lon):
        query = """
        MATCH (l:Location)-[:HAS_WEATHER]->(w:Weather)
        WHERE point.distance(
            point({latitude:l.lat, longitude:l.lon}),
            point({latitude:$lat, longitude:$lon})
        ) < 2000
        RETURN
            avg(w.temperature) AS avg_temp,
            avg(w.windspeed) AS avg_wind,
            count(w) AS weather_points
        """

        records = self.conn.execute(query, {
            "lat": (src_lat + dst_lat) / 2,
            "lon": (src_lon + dst_lon) / 2
        })

        if not records:
            return "No contextual graph data available."

        rec = records[0]

        # ✅ SAFE HANDLING (THIS IS THE FIX)
        temp = rec["avg_temp"]
        wind = rec["avg_wind"]
        count = rec["weather_points"]

        context_parts = []

        if temp is not None:
            context_parts.append(f"Average nearby temperature is {round(temp,1)}°C")
        else:
            context_parts.append("Temperature data is partially unavailable")

        if wind is not None:
            context_parts.append(f"Average wind speed is {round(wind,1)} km/h")

        context_parts.append(f"Based on {count} nearby road segments")

        return ". ".join(context_parts) + "."
