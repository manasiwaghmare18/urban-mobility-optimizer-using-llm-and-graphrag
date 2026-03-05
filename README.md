# 🚦Urban Mobility Optimizer using LLM and GraphRAG

# 📌 Project Overview

The Urban Mobility Optimizer using LLM and GraphRAG is an intelligent urban travel analysis system that helps users choose the most suitable transportation option within a city environment, specifically Hyderabad.

Traditional navigation systems only provide route suggestions and estimated travel time. However, they do not explain why one transport option is better than another. This project addresses that gap by integrating Graph Databases, Agent-based AI architecture, and Large Language Models (LLMs) to generate explainable travel recommendations.

# The system evaluates multiple factors including:

Route distance

Travel cost

Travel time

Transport availability

Weather conditions

By combining GraphRAG and LLM reasoning, the system generates clear, data-driven insights that help users make better transportation decisions.

# 🎯 Problem Statement

Urban commuters often choose transportation modes without structured comparison of cost, time, or availability.

Existing navigation systems:

Show routes but not reasoning

Do not compare transport options effectively

Provide limited decision support

This project solves this problem by creating a system that performs multi-factor travel analysis and generates explainable recommendations using AI.

# 🚀 Key Features

Graph-based shortest path computation using Neo4j

Travel cost estimation for Car, Bus, and Metro

Travel time comparison across transport modes

Detection of public transport availability

Real-time weather data integration

GraphRAG-based contextual reasoning

AI-generated explanations using LLM (Gemma via Ollama)

Interactive Streamlit dashboard

Cost vs Travel Time comparison visualization

Map-based route display

# 🧠 System Architecture

The system follows a Fully Agentic AI Architecture where different agents handle specialized tasks.

# User Input (Streamlit UI)
        │
        ▼
# Orchestrator Agent
        │
        ├── Route Agent
        │       → Computes shortest path using Neo4j
        │
        ├── Weather Agent
        │       → Fetches weather data using Open-Meteo API
        │
        ├── Cost Agent
        │       → Calculates travel cost and time
        │
        ├── Transport Agent
        │       → Detects bus and metro availability
        │
        ├── GraphRAG Context Builder
        │       → Retrieves graph context from Neo4j
        │
        ▼
# LLM (Gemma via Ollama)
        │
        ▼
# Explainable Transport Recommendation
# 🗂 Project Structure
project/
│
├── agents/                      # AI agents
│   ├── route_agent.py
│   ├── weather_agent.py
│   ├── cost_agent.py
│   ├── transport_agent.py
│   └── orchestrator.py
│
├── config/
│   └── settings.py              # Configuration settings
│
├── data/
│   └── bus_stops.csv            # Bus stop dataset
│
├── data_ingestion/              # Data collection and preprocessing
│
├── graph_db/
│   └── neo4j_connection.py      # Neo4j database connection
│
├── llm/
│   └── explanation_generator.py # LLM explanation generation
│
├── ui/
│   └── app.py                   # Streamlit UI
│
├── run_graph_load.py            # Graph loading script
├── test_agents.py
├── test_agents_stepwise.py
└── test_weather_mapping.py

# 🛠 Technologies Used
# Programming Language:
- Python
- Graph Database
- Neo4j
- AI / LLM
- Ollama
- Gemma Model
- Data Processing
- Pandas
- OSMnx
- NetworkX
- Visualization
- Matplotlib
- Streamlit

# APIs
- OpenStreetMap (Road network data)
- Open-Meteo API (Weather data)

# 📦 Requirements

# Create a file called requirements.txt

streamlit
pandas
numpy
matplotlib
requests
neo4j
osmnx
networkx
geopandas

# Install dependencies:

pip install -r requirements.txt
⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/your-username/urban-mobility-optimizer.git
cd urban-mobility-optimizer
2️⃣ Create Virtual Environment
python -m venv venv

# Activate environment:

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Install Neo4j

# Download Neo4j Desktop

Create a database and update credentials in:

config/settings.py

Example configuration:

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"
NEO4J_DATABASE = "projectdb"

Start the Neo4j database before running the application.

# 5️⃣ Load Graph Data

Run the graph ingestion script:

python run_graph_load.py

This script loads road network and transport data into Neo4j.

# 6️⃣ Install Ollama

Download Ollama from:

https://ollama.com

Pull the Gemma model:

ollama pull gemma3
# 7️⃣ Run the Application
streamlit run ui/app.py

# Open browser:

http://localhost:8501
📊 Example Output

# The system displays:

Route distance

Weather conditions

Transport availability

Cost comparison table

Travel time comparison

AI-generated explanation

Cost vs Time visualization chart

Map showing selected route

# 🔮 Future Improvements

Possible enhancements include:

Integration of live traffic data

Multi-city expansion

Carbon emission analysis for transport modes

Personalized travel recommendations

Voice-based interface

# 👨‍💻 Authors

Mansi Omprakash Waghmare
PG-DBDA
C-DAC Hyderabad
