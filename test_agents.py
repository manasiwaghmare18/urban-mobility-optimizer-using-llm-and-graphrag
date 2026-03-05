from graph_db.neo4j_connection import Neo4jConnection
from agents.orchestrator import OrchestratorAgent

def main():
    print("=== TESTING FULL AGENTIC AI PIPELINE ===")

    source = (17.4375, 78.4483)   # Ameerpet
    destination = (17.4401, 78.3489)  # Gachibowli

    conn = Neo4jConnection()
    orchestrator = OrchestratorAgent(conn)

    result = orchestrator.handle_request(source, destination)
    conn.close()

    for k, v in result.items():
        print(f"{k}: {v}")

    print("\n✅ Fully Agentic Pipeline Test Completed")

if __name__ == "__main__":
    main()
