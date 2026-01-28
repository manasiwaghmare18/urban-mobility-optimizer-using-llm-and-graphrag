class TransportAgent:
    def __init__(self, conn):
        self.conn = conn

    def check_availability(self, src_lat, src_lon, dst_lat, dst_lon):
        """
        Check whether bus or metro is available
        near either source or destination.
        """

        query = """
        // -------- BUS CHECK --------
        MATCH (b:BusStop)
        WHERE
          point.distance(
            point({latitude: b.lat, longitude: b.lon}),
            point({latitude: $src_lat, longitude: $src_lon})
          ) < 1000
          OR
          point.distance(
            point({latitude: b.lat, longitude: b.lon}),
            point({latitude: $dst_lat, longitude: $dst_lon})
          ) < 1000
        WITH count(b) AS bus_count

        // -------- METRO CHECK --------
        MATCH (m:MetroStation)
        WHERE
          point.distance(
            point({latitude: m.lat, longitude: m.lon}),
            point({latitude: $src_lat, longitude: $src_lon})
          ) < 1500
          OR
          point.distance(
            point({latitude: m.lat, longitude: m.lon}),
            point({latitude: $dst_lat, longitude: $dst_lon})
          ) < 1500

        RETURN
          bus_count > 0 AS bus_available,
          count(m) > 0 AS metro_available
        """

        result = self.conn.execute(query, {
            "src_lat": float(src_lat),
            "src_lon": float(src_lon),
            "dst_lat": float(dst_lat),
            "dst_lon": float(dst_lon)
        })

        # Neo4j returns a list → handle safely
        if not result or len(result) == 0:
            return {
                "bus_available": False,
                "metro_available": False
            }

        record = result[0]

        return {
            "bus_available": bool(record["bus_available"]),
            "metro_available": bool(record["metro_available"])
        }
