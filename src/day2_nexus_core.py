"""
NEXUS-CORE LOGISTICS INTELLIGENCE SYSTEM
Day 2 – Hybrid Risk Engine + Multi-Agent Swarm Optimization

Features:
- 20 City Logistics Network
- Hybrid Risk Engine (Weather + Traffic)
- Multi-Agent Debate (LangGraph)
- Route Optimization using NetworkX
- Visualization of Optimal Route
"""

# ================================
# IMPORTS
# ================================

import networkx as nx
import random
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph


# ================================
# STEP 1: CREATE LOGISTICS NETWORK
# ================================

G = nx.Graph()

# Create 20 City Nodes
cities = [f"City-{i}" for i in range(1, 21)]
G.add_nodes_from(cities)

# Add Random Routes (Edges)
for _ in range(45):
    city_a, city_b = random.sample(cities, 2)
    distance = random.randint(50, 500)  # Distance in km
    G.add_edge(city_a, city_b, distance=distance)

print("🔥 Logistics Graph Ready")
print("Total Cities:", len(G.nodes))
print("Total Routes:", len(G.edges))


# ================================
# STEP 2: HYBRID RISK ENGINE
# ================================

def risk_penalty():
    """
    Hybrid Risk Model:
    - Weather Delay (0–30%)
    - Traffic Delay (0–20%)
    """
    weather_delay = random.uniform(0, 0.3)
    traffic_delay = random.uniform(0, 0.2)
    return weather_delay + traffic_delay


# Apply Risk to Each Route
for u, v in G.edges():
    base_distance = G[u][v]["distance"]
    penalty = risk_penalty()
    G[u][v]["cost"] = base_distance * (1 + penalty)

print("⚡ Hybrid Risk Model Applied (Weather + Traffic)")


# ================================
# STEP 3: VISUALIZE NETWORK
# ================================

plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, node_size=300, with_labels=True)
plt.title("🌍 Nexus-Core Logistics Network (Day 2)")
plt.show()


# ================================
# STEP 4: MULTI-AGENT SWARM SYSTEM
# ================================

def analyst_agent(state):
    state["debate"].append(
        f"📊 Analyst: Evaluating routes from {state['source']} → {state['target']}"
    )
    return state


def risk_agent(state):
    state["debate"].append(
        "⚠️ Risk Agent: Weather and Traffic delays incorporated into cost."
    )
    return state


def strategist_agent(state):
    state["debate"].append(
        "🧠 Strategist: Selecting route with minimum hybrid cost."
    )
    return state


def optimizer_agent(state):
    source = state["source"]
    target = state["target"]

    # Compute shortest path using hybrid cost
    path = nx.shortest_path(G, source, target, weight="cost")

    total_cost = sum(
        G[path[i]][path[i + 1]]["cost"]
        for i in range(len(path) - 1)
    )

    state["best_path"] = path
    state["total_cost"] = total_cost

    state["debate"].append(
        f"✅ Optimizer: Best Route = {path} | Total Cost = {total_cost:.2f}"
    )
    return state


# ================================
# STEP 5: BUILD SWARM WORKFLOW
# ================================

workflow = StateGraph(dict)

workflow.add_node("Analyst", analyst_agent)
workflow.add_node("Risk", risk_agent)
workflow.add_node("Strategist", strategist_agent)
workflow.add_node("Optimizer", optimizer_agent)

workflow.set_entry_point("Analyst")

workflow.add_edge("Analyst", "Risk")
workflow.add_edge("Risk", "Strategist")
workflow.add_edge("Strategist", "Optimizer")

swarm_app = workflow.compile()

print("🔥 Nexus Swarm Ready (Day 2)")


# ================================
# STEP 6: EXECUTE ROUTE DECISION
# ================================

source, target = random.sample(cities, 2)

state = {
    "source": source,
    "target": target,
    "debate": []
}

result = swarm_app.invoke(state)

print("\n==============================")
print("🏛️ NEXUS-CORE ROUTING DECISION")
print("==============================\n")

print("SOURCE:", source)
print("TARGET:", target)

print("\n--- AGENT DEBATE LOG ---\n")
for log in result["debate"]:
    print(log)

print("\n--- FINAL OPTIMAL ROUTE ---\n")
print("Best Path:", result["best_path"])
print("Total Hybrid Cost:", round(result["total_cost"], 2))


# ================================
# STEP 7: HIGHLIGHT OPTIMAL ROUTE
# ================================

best_path = result["best_path"]

plt.figure(figsize=(10, 7))
nx.draw(G, pos, node_size=250, with_labels=True)

highlight_edges = list(zip(best_path, best_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, width=4)

plt.title("🔥 Nexus-Core Optimal Route (Day 2)")
plt.show()

