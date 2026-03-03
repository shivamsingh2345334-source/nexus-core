# ==========================================
# NEXUS-NEURAL-CORE: SINGLE-CELL DEPLOYMENT
# Architect: SHIVAM
# ==========================================

import os
import sys
import logging
import asyncio
import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import nest_asyncio
from langgraph.graph import StateGraph

# --- SECTION 1: CONFIGURATION ---
NEXUS_CONFIG = {
    "LEARNING_RATE": 0.03,
    "WEIGHT_BOUNDS": (0.1, 0.9),
    "NODE_COUNT": 20,
    "LOG_LEVEL": logging.INFO
}

# --- SECTION 2: TELEMETRY & LOGGING ---
logging.basicConfig(
    level=NEXUS_CONFIG["LOG_LEVEL"],
    format='%(asctime)s | %(levelname)s | ARCHITECT: SHIVAM | %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger("Nexus-Neural-Core")

# --- SECTION 3: SOVEREIGN ADAPTIVE ROUTER ---
class SovereignAdaptiveRouter:
    def __init__(self):
        self.w_cost = 0.5
        self.w_risk = 0.5
        self.history = []

    def compute_hybrid_score(self, cost, risk):
        return (self.w_cost * cost) + (self.w_risk * risk)

    def evolve_weights(self, cost, risk):
        try:
            # Neural Adjustment Logic
            if risk > (cost / 100):
                self.w_risk += NEXUS_CONFIG["LEARNING_RATE"]
                self.w_cost -= NEXUS_CONFIG["LEARNING_RATE"]
                reason = "Risk Escalation"
            else:
                self.w_cost += NEXUS_CONFIG["LEARNING_RATE"]
                self.w_risk -= NEXUS_CONFIG["LEARNING_RATE"]
                reason = "Cost Optimization"

            # Bound Enforcement (Clipping)
            low, high = NEXUS_CONFIG["WEIGHT_BOUNDS"]
            self.w_cost = np.clip(self.w_cost, low, high)
            self.w_risk = np.clip(self.w_risk, low, high)
            return reason
        except Exception as e:
            logger.error(f"Neural Evolution Failed: {e}")
            return "Stable"

# --- SECTION 4: SIMULATION ENGINE (GRAPH BUILDER) ---
def build_graph(node_count):
    # Generating a random network topology
    G = nx.fast_gnp_random_graph(node_count, 0.4)
    for (u, v) in G.edges():
        G[u][v]["distance"] = np.random.randint(50, 400)
        G[u][v]["risk"] = np.random.uniform(0.05, 0.4)
    return G

# --- SECTION 5: SWARM INTELLIGENCE (LANGGRAPH WORKFLOW) ---
class SwarmIntelligence:
    def __init__(self, G, router):
        self.G = G
        self.router = router
        self.workflow = self._build_swarm()

    def _build_swarm(self):
        def analyst(state):
            state["debate"].append("Analyst: Network scanned.")
            return state

        def optimizer(state):
            # Pathfinding via Dijkstra's algorithm logic
            path = nx.shortest_path(self.G, state["source"], state["target"], weight="distance")
            cost = sum(self.G[path[i]][path[i+1]]["distance"] for i in range(len(path)-1))
            risk = sum(self.G[path[i]][path[i+1]]["risk"] for i in range(len(path)-1))
            
            score = self.router.compute_hybrid_score(cost, risk)
            reason = self.router.evolve_weights(cost, risk)
            
            # Recording telemetry for plotting
            self.router.history.append({
                "cost": cost, "risk": risk, "w_cost": self.router.w_cost, 
                "w_risk": self.router.w_risk, "reason": reason
            })
            state["result"] = f"Path Locked | Score: {score:.2f}"
            return state

        # Define Graph State Logic
        graph = StateGraph(dict)
        graph.add_node("Analyst", analyst)
        graph.add_node("Optimizer", optimizer)
        graph.set_entry_point("Analyst")
        graph.add_edge("Analyst", "Optimizer")
        return graph.compile()

# --- SECTION 6: MAIN EXECUTION & VISUALIZATION ---
async def run_simulation():
    # Initialization
    G = build_graph(NEXUS_CONFIG["NODE_COUNT"])
    router = SovereignAdaptiveRouter()
    swarm = SwarmIntelligence(G, router)

    logger.info("Starting Nexus Neural Swarm Simulation...")

    # Running 15 dynamic routing iterations
    for i in range(15):
        s, t = random.sample(list(G.nodes), 2)
        await swarm.workflow.ainvoke({
            "source": s, "target": t, "debate": []
        })

    # Processing History and Plotting Results
    df = pd.DataFrame(router.history)
    
    plt.figure(figsize=(12, 6))
    plt.plot(df["w_cost"], label="Cost Weight (Efficiency)", color='#3498db', linewidth=2, marker='o')
    plt.plot(df["w_risk"], label="Risk Weight (Safety)", color='#e74c3c', linewidth=2, marker='s')
    
    plt.title("Nexus-Neural-Core: Autonomous Weight Evolution", fontsize=14)
    plt.xlabel("Simulation Steps", fontsize=12)
    plt.ylabel("Weight Value", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()

    print("\n✅ SUCCESS: Intelligence Mesh Evolved.")

# Apply Nest Asyncio for Colab/Jupyter compatibility
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(run_simulation())
