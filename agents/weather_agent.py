from data_ingestion.weather_scraper import fetch_realtime_weather

class WeatherAgent:
    def analyze(self, lat, lon):
        weather = fetch_realtime_weather(lat, lon)

        if not weather:
            return {
                "avg_temperature": None,
                "avg_windspeed": None
            }

        return {
            "avg_temperature": weather["temperature"],
            "avg_windspeed": weather["windspeed"]
        }
