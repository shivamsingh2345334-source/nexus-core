import requests
import random
import time
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph

# --- CORE LOGIC: Perception Engine ---
class PerceptionEngine:
    """Fetches real-time environmental data and simulates logistics nodes."""
    
    def fetch_weather(self):
        # Fetching live data for Delhi (Latitude: 28.61, Longitude: 77.20)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 28.61,
            "longitude": 77.20,
            "current_weather": True
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            return {
                "temperature": data["current_weather"]["temperature"],
                "windspeed": data["current_weather"]["windspeed"]
            }
        except Exception as e:
            print(f"⚠️ Weather API Error: {e}")
            return {"temperature": 25, "windspeed": 10} # Fallback

    def simulated_logistics_nodes(self, n=8):
        return [
            {
                "id": f"Truck-{i}",
                "x": random.uniform(10, 90),
                "y": random.uniform(10, 90),
                "load": random.randint(1, 10)
            }
            for i in range(n)
        ]

    def get_world_state(self):
        return {
            "weather": self.fetch_weather(),
            "logistics_nodes": self.simulated_logistics_nodes(),
            "analysis": ""
        }

# --- AI AGENT: Nexus Swarm (LangGraph) ---
class NexusSwarm:
    """Agentic workflow to analyze logistics based on environmental context."""
    
    def __init__(self):
        def analyst_agent(state):
            weather = state["weather"]
            nodes = state["logistics_nodes"]
            
            # Smart Analysis Logic
            state["analysis"] = (
                f"📌 NEXUS ANALYST REPORT\n"
                f"----------------------\n"
                f"🌡️ Temperature: {weather['temperature']}°C\n"
                f"💨 Wind Speed : {weather['windspeed']} km/h\n"
                f"🚚 Active Fleet: {len(nodes)} Units\n"
                f"STATUS: {'High Risk - Monitor Wind' if weather['windspeed'] > 15 else 'All Clear'}"
            )
            return state

        # Building the Graph
        workflow = StateGraph(dict)
        workflow.add_node("Analyst", analyst_agent)
        workflow.set_entry_point("Analyst")
        self.app = workflow.compile()

    def run(self, world_state):
        return self.app.invoke(world_state)

# --- VISUALIZATION: Simulation Engine ---
def run_simulation(steps=3):
    engine = PerceptionEngine()
    swarm = NexusSwarm()
    
    # Initialize World
    world_state = engine.get_world_state()
    nodes = world_state["logistics_nodes"]

    print("🚀 Nexus-Core Initialized...")
    
    for step in range(steps):
        # 1. Run AI Agent Analysis
        result = swarm.run(world_state)
        print(f"\n--- Step {step + 1} ---")
        print(result["analysis"])

        # 2. Update Visuals
        plt.figure(figsize=(10, 7))
        
        # Move nodes dynamically
        for n in nodes:
            n["x"] += random.uniform(-5, 5)
            n["y"] += random.uniform(-5, 5)
            # Boundary checks
            n["x"] = max(0, min(100, n["x"]))
            n["y"] = max(0, min(100, n["y"]))

        x_coords = [n["x"] for n in nodes]
        y_coords = [n["y"] for n in nodes]

        plt.scatter(x_coords, y_coords, s=100, c='blue', alpha=0.6, edgecolors='black')
        
        for n in nodes:
            plt.text(n["x"]+1, n["y"]+1, n["id"], fontsize=9, fontweight='bold')

        plt.title(f"🚚 Nexus-Core Live Logistics Grid | Step {step+1}\nTemp: {world_state['weather']['temperature']}°C", fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.show()
        
        time.sleep(1)

# --- EXECUTION ---
if __name__ == "__main__":
    run_simulation(steps=3)
