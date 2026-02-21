# ===============================
# DAY 4 — Parallel Multi-Agent Engine
# ===============================

import requests
import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from concurrent.futures import ThreadPoolExecutor


# =====================================
# Mock Graph + Router Setup (Required)
# =====================================

G = nx.Graph()

cities = ["Delhi","Mumbai","Chennai","Kolkata","Bangalore","Hyderabad"]

for city in cities:
    G.add_node(city)

for i in range(len(cities)):
    for j in range(i+1,len(cities)):
        G.add_edge(
            cities[i],
            cities[j],
            distance=random.randint(50,500),
            risk=random.uniform(0.1,0.9)
        )


class AdaptiveRouter:

    def __init__(self):
        self.weight_cost = 0.5
        self.weight_risk = 0.5
        self.history = []

    def compute_score(self,cost,risk):
        return (cost*self.weight_cost)+(risk*100*self.weight_risk)

    def update_weights(self,cost,risk):
        if risk > 0.5:
            self.weight_risk += 0.01
            self.weight_cost -= 0.01
        else:
            self.weight_cost += 0.01
            self.weight_risk -= 0.01

        self.weight_cost = max(0.1,min(0.9,self.weight_cost))
        self.weight_risk = max(0.1,min(0.9,self.weight_risk))

    def log(self,path,cost,risk,score):
        self.history.append({
            "path":path,
            "cost":cost,
            "risk":risk,
            "score":score
        })


router = AdaptiveRouter()


# =====================================
# Hybrid Risk Engine
# =====================================

def fetch_real_weather_risk():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 28.61,
            "longitude": 77.20,
            "current_weather": True
        }
        data = requests.get(url, params=params, timeout=3).json()
        wind = data["current_weather"]["windspeed"]
        return min(wind/100,0.3)

    except:
        return random.uniform(0.05,0.25)


# =====================================
# Parallel Agents
# =====================================

def parallel_agents(state):

    start_time = time.time()

    def analyst():
        return "Analyst: Network metrics evaluated."

    def risk():
        real_risk = fetch_real_weather_risk()
        return f"Risk Agent: external factor={round(real_risk,3)}"

    def strategist():
        return "Strategist: Hybrid adaptive scoring active."

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(analyst),
            executor.submit(risk),
            executor.submit(strategist)
        ]
        results = [f.result() for f in futures]

    state["debate"].extend(results)
    state["agent_parallel_time"] = time.time() - start_time

    return state


# =====================================
# Optimizer
# =====================================

def optimized_decision(state):

    start_time = time.time()

    source = state["source"]
    target = state["target"]

    path = nx.shortest_path(G,source,target,weight="distance")

    total_cost = 0
    total_risk = 0

    for i in range(len(path)-1):
        edge = G[path[i]][path[i+1]]
        total_cost += edge["distance"]
        total_risk += edge["risk"]

    score = router.compute_score(total_cost,total_risk)
    router.update_weights(total_cost,total_risk)
    router.log(path,total_cost,total_risk,score)

    state["optimizer_time"] = time.time() - start_time
    state["score"] = score

    state["debate"].append(
        f"Optimizer: Cost={round(total_cost,2)} | "
        f"Risk={round(total_risk,2)} | Score={round(score,2)}"
    )

    return state


# =====================================
# Parallel Batch Execution
# =====================================

def run_parallel_batch(batch_size=20):

    results=[]
    start_batch=time.time()

    def single_decision():

        source,target=random.sample(cities,2)

        state={
            "source":source,
            "target":target,
            "debate":[]
        }

        state=parallel_agents(state)
        state=optimized_decision(state)

        state["total_decision_time"]=(
            state["agent_parallel_time"]+
            state["optimizer_time"]
        )

        return state

    with ThreadPoolExecutor() as executor:
        futures=[executor.submit(single_decision) for _ in range(batch_size)]
        for f in futures:
            results.append(f.result())

    batch_time=time.time()-start_batch

    print("\nBatch Completed")
    print("Total Batch Time:",round(batch_time,3),"seconds")

    return results


# =====================================
# Run Engine
# =====================================

if __name__ == "__main__":

    batch_results=run_parallel_batch()


    analytics=[]

    for r in batch_results:
        analytics.append({
            "score":r["score"],
            "agent_parallel_time":r["agent_parallel_time"],
            "optimizer_time":r["optimizer_time"],
            "total_decision_time":r["total_decision_time"],
            "weight_cost":router.weight_cost,
            "weight_risk":router.weight_risk
        })

    analytics_df=pd.DataFrame(analytics)

    print("\nAnalytics Sample:")
    print(analytics_df.head())


    plt.figure(figsize=(10,6))
    plt.plot(analytics_df["total_decision_time"].values)
    plt.title("Decision Latency per Execution")
    plt.xlabel("Decision #")
    plt.ylabel("Time (seconds)")
    plt.show()
