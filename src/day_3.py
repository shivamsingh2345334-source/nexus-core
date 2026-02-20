"""
NEXUS CORE — Adaptive Logistics Intelligence System
Author: YourName
Description:
Multi-Agent + Adaptive Routing Simulation
"""

import networkx as nx
import random
import pandas as pd
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph


# =====================================================
# 1. GRAPH BUILDER
# =====================================================

random.seed(42)

def build_logistics_graph(num_cities=20, num_routes=50):
    G = nx.Graph()

    cities = [f"City-{i}" for i in range(1, num_cities + 1)]
    G.add_nodes_from(cities)

    for _ in range(num_routes):
        a, b = random.sample(cities, 2)

        distance = random.randint(50, 400)
        weather_risk = random.uniform(0.05, 0.25)
        traffic_risk = random.uniform(0.05, 0.20)

        total_risk = weather_risk + traffic_risk

        G.add_edge(
            a, b,
            distance=distance,
            risk=total_risk
        )

    return G


G = build_logistics_graph()
cities = list(G.nodes)

print("✅ Graph Ready")
print("Cities:", len(G.nodes))
print("Routes:", len(G.edges))


# =====================================================
# 2. ADAPTIVE ROUTER
# =====================================================

class AdaptiveRouter:

    def __init__(self):
        self.weight_cost = 0.5
        self.weight_risk = 0.5
        self.logs = []

    def compute_score(self, total_cost, total_risk):
        return (
            self.weight_cost * total_cost +
            self.weight_risk * total_risk
        )

    def update_weights(self, total_cost, total_risk):

        if total_risk > total_cost:
            self.weight_risk += 0.03
            self.weight_cost -= 0.03
        else:
            self.weight_cost += 0.03
            self.weight_risk -= 0.03

        # safety clamp
        self.weight_cost = max(0.1, min(0.9, self.weight_cost))
        self.weight_risk = max(0.1, min(0.9, self.weight_risk))

    def log(self, route, cost, risk, score):
        self.logs.append({
            "route": str(route),
            "cost": cost,
            "risk": risk,
            "score": score,
            "weight_cost": self.weight_cost,
            "weight_risk": self.weight_risk
        })

    def dataframe(self):
        return pd.DataFrame(self.logs)


router = AdaptiveRouter()
print("✅ Adaptive Router Initialized")


# =====================================================
# 3. AGENT DEFINITIONS
# =====================================================

def analyst_agent(state):
    state["debate"].append("📊 Analyst: Evaluating network metrics.")
    return state


def risk_agent(state):
    state["debate"].append("⚠️ Risk Agent: Weather + Traffic risk applied.")
    return state


def strategist_agent(state):
    state["debate"].append("🧠 Strategist: Optimizing adaptive hybrid score.")
    return state


def optimizer_agent(state):

    source = state["source"]
    target = state["target"]

    path = nx.shortest_path(G, source, target, weight="distance")

    total_cost = 0
    total_risk = 0

    for i in range(len(path) - 1):
        edge = G[path[i]][path[i+1]]
        total_cost += edge["distance"]
        total_risk += edge["risk"]

    score = router.compute_score(total_cost, total_risk)
    router.update_weights(total_cost, total_risk)
    router.log(path, total_cost, total_risk, score)

    state["debate"].append(
        f"🔥 Optimizer: Route={path} | Cost={round(total_cost,2)} | "
        f"Risk={round(total_risk,2)} | Score={round(score,2)}"
    )

    return state


# =====================================================
# 4. BUILD SWARM
# =====================================================

workflow = StateGraph(dict)

workflow.add_node("Analyst", analyst_agent)
workflow.add_node("Risk", risk_agent)
workflow.add_node("Strategist", strategist_agent)
workflow.add_node("Optimizer", optimizer_agent)

workflow.set_entry_point("Analyst")

workflow.add_edge("Analyst", "Risk")
workflow.add_edge("Risk", "Strategist")
workflow.add_edge("Strategist", "Optimizer")

swarm = workflow.compile()

print("✅ Swarm Compiled")


# =====================================================
# 5. RUN MULTIPLE DECISIONS
# =====================================================

for i in range(15):

    source, target = random.sample(cities, 2)

    state = {
        "source": source,
        "target": target,
        "debate": []
    }

    result = swarm.invoke(state)

    print(f"\n=== Decision {i+1} ===")
    for line in result["debate"]:
        print(line)


# =====================================================
# 6. LOG DATAFRAME
# =====================================================

df = router.dataframe()

print("\n📊 Log Preview")
print(df.head())
print("\nColumns:", df.columns)


# =====================================================
# 7. WEIGHT EVOLUTION GRAPH
# =====================================================

plt.figure(figsize=(8,5))

plt.plot(df["weight_cost"].values, label="Cost Weight")
plt.plot(df["weight_risk"].values, label="Risk Weight")

plt.title("Adaptive Cost-Risk Weight Evolution")
plt.xlabel("Decision Step")
plt.ylabel("Weight")
plt.legend()

plt.show()
