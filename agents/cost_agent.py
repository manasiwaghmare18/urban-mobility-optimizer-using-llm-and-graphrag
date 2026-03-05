class CostAgent:
    def estimate(self, distance_m):
        """
        Estimate travel cost and travel time for different transport modes.
        distance_m: distance in meters
        """
        km = distance_m / 1000

        # Average speeds (km/h) — documented assumptions
        CAR_SPEED = 25
        BUS_SPEED = 18
        METRO_SPEED = 35

        return {
            # 💰 Cost (₹)
            "car_cost_rs": round(km * 12, 2),
            "bus_cost_rs": round(km * 2, 2),
            "metro_cost_rs": round(km * 3, 2),

            # ⏱️ Travel Time (minutes)
            "car_time_min": round((km / CAR_SPEED) * 60, 1),
            "bus_time_min": round((km / BUS_SPEED) * 60, 1),
            "metro_time_min": round((km / METRO_SPEED) * 60, 1),
        }

