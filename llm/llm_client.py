import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:latest"


def generate_explanation(route, weather, cost, transport):
    """
    Generate strict explanation-only output using local Ollama LLM.
    Includes explicit cost-best and time-best statements.
    """

    prompt = f"""
You are a senior urban mobility analyst preparing a professional explanation.

STRICT RULES (MANDATORY):
- Do NOT ask any questions
- Do NOT invite user interaction
- Do NOT use conversational phrases
- Do NOT end with a question
- Explain only using provided data
- Include explicit cost-based and time-based conclusions

==================================================
ROUTE OVERVIEW
==================================================
The total travel distance for this journey is {route['distance_km']} km.
This distance represents a typical urban trip within Hyderabad,
requiring consideration of traffic, connectivity, and transport efficiency.

==================================================
WEATHER CONDITIONS
==================================================
The observed weather conditions are:
- Temperature: {weather.get('avg_temperature')}°C
- Wind speed: {weather.get('avg_windspeed')} km/h

These conditions are generally suitable for travel and do not
significantly restrict road or public transport operations.

==================================================
TRANSPORT OPTIONS ANALYSIS
==================================================

CAR:
- Cost: ₹{cost['car_cost_rs']}
- Travel time: {cost['car_time_min']} minutes

BUS:
- Cost: ₹{cost['bus_cost_rs']}
- Travel time: {cost['bus_time_min']} minutes
- Available: {transport['bus_available']}

METRO:
- Cost: ₹{cost['metro_cost_rs']}
- Travel time: {cost['metro_time_min']} minutes
- Available: {transport['metro_available']}

==================================================
COST-BASED COMPARISON
==================================================
When comparing only the travel cost, the cheapest available transport
option should be preferred for budget efficiency.
Clearly state which transport mode has the lowest cost
and explain why it is economically advantageous.

==================================================
TIME-BASED COMPARISON
==================================================
When comparing only travel time, the fastest available transport
option should be preferred for time efficiency.
Clearly state which transport mode requires the least travel time
and explain why it is faster.

==================================================
FINAL BALANCED RECOMMENDATION
==================================================
Provide a final recommendation that balances:
- Cost
- Travel time
- Transport availability
- Urban travel practicality

State clearly:
- Which option is best by cost
- Which option is best by time
- Which option is the most balanced overall choice

End the explanation after the recommendation.
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        text = response.json().get("response", "").strip()

        # ----------------------------------
        # HARD FILTER: REMOVE QUESTIONS
        # ----------------------------------
        forbidden_phrases = [
            "Would you like",
            "Do you want",
            "Let me know",
            "I can help",
            "You may want",
            "Should you"
        ]

        for phrase in forbidden_phrases:
            if phrase in text:
                text = text.split(phrase)[0].strip()

        return text

    except Exception:
        return (
            "The AI explanation could not be generated at this moment. "
            "The analysis above is based on system-generated results."
        )
