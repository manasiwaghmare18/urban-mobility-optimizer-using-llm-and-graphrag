class RouteAgent:
    def __init__(self, conn):
        self.conn = conn

    def find_route(self, src_lat, src_lon, dst_lat, dst_lon):
        query = """
        // 1️⃣ Candidate source nodes
        MATCH (s:Location)
        WITH s,
             point.distance(
               point({latitude:s.lat, longitude:s.lon}),
               point({latitude:$slat, longitude:$slon})
             ) AS sd
        ORDER BY sd
        LIMIT 5

        // 2️⃣ Candidate destination nodes
        MATCH (d:Location)
        WITH s, d,
             point.distance(
               point({latitude:d.lat, longitude:d.lon}),
               point({latitude:$dlat, longitude:$dlon})
             ) AS dd
        ORDER BY dd
        LIMIT 5

        // 3️⃣ Shortest path with safe hop limit
        MATCH p = shortestPath((s)-[:CONNECTS*..120]->(d))
        WITH reduce(dist = 0.0, r IN relationships(p) | dist + r.length) AS total_dist
        RETURN total_dist
        ORDER BY total_dist
        LIMIT 1
        """

        records = self.conn.execute(query, {
            "slat": src_lat,
            "slon": src_lon,
            "dlat": dst_lat,
            "dlon": dst_lon
        })

        if not records:
            return None

        return {"distance_m": records[0]["total_dist"]}
