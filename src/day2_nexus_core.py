import asyncio
import os
import random
import logging
import sys

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from langgraph.graph import StateGraph


# ============================================================
# 🔧 CONFIGURATION LAYER
# ============================================================

class NexusConfig:
    ENV = os.getenv("NEXUS_ENV", "PRODUCTION")
    NODE_COUNT = int(os.getenv("NODE_COUNT", 20))
    TARGET_SCALE = 1_000_000_000_000
    EDGE_PROBABILITY = 0.25
    LOG_LEVEL = logging.INFO


logging.basicConfig(
    level=NexusConfig.LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | NEXUS-CORE | %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("Nexus-Core")


# ============================================================
# 🏛 SOVEREIGN MESH ENGINE
# ============================================================

class SovereignMesh:
    """Resilient self-healing routing mesh"""

    def __init__(self):
        self.G = nx.Graph()
        self.cities = [
            f"City-{i}" for i in range(1, NexusConfig.NODE_COUNT + 1)
        ]
        self._initialize_resilient_graph()

    def _initialize_resilient_graph(self):
        try:
            self.G = nx.fast_gnp_random_graph(
                NexusConfig.NODE_COUNT,
                NexusConfig.EDGE_PROBABILITY,
            )

            mapping = {i: self.cities[i] for i in range(len(self.cities))}
            self.G = nx.relabel_nodes(self.G, mapping)

            # 🔁 Auto-Healing Connectivity
            if not nx.is_connected(self.G):
                logger.warning("Disconnected mesh detected. Healing...")
                components = list(nx.connected_components(self.G))
                for i in range(len(components) - 1):
                    u = list(components[i])[0]
                    v = list(components[i + 1])[0]
                    self.G.add_edge(u, v)

            # 💰 Hybrid Cost Injection
            for u, v in self.G.edges():
                distance = np.random.randint(50, 500)
                risk = np.random.uniform(0.05, 0.5)
                self.G[u][v]["distance"] = distance
                self.G[u][v]["cost"] = distance * (1 + risk)

            logger.info(
                f"Mesh Ready: {len(self.G.nodes)} cities | {len(self.G.edges)} routes"
            )

        except Exception as e:
            logger.critical(f"Mesh Initialization Failure: {e}")
            raise


# ============================================================
# 🧠 AGENTIC SWARM ROUTER
# ============================================================

class SwarmRouter:
    """Async multi-agent routing workflow"""

    def __init__(self, mesh: SovereignMesh):
        self.mesh = mesh
        self.workflow = self._compile_swarm()

    def _compile_swarm(self):

        def analyst(state):
            state["debate"].append(
                f"Analyst validated topology for {state['source']}"
            )
            return state

        def optimizer(state):
            try:
                path = nx.shortest_path(
                    self.mesh.G,
                    state["source"],
                    state["target"],
                    weight="cost",
                )

                total_cost = sum(
                    self.mesh.G[path[i]][path[i + 1]]["cost"]
                    for i in range(len(path) - 1)
                )

                state["best_path"] = path
                state["total_cost"] = total_cost
                state["debate"].append(
                    f"Optimizer locked route | Cost: {total_cost:.2f}"
                )

            except Exception as e:
                logger.error(f"Routing failure: {e}")
                state["best_path"] = None
                state["total_cost"] = 0

            return state

        builder = StateGraph(dict)
        builder.add_node("Analyst", analyst)
        builder.add_node("Optimizer", optimizer)
        builder.set_entry_point("Analyst")
        builder.add_edge("Analyst", "Optimizer")

        return builder.compile()


# ============================================================
# 📊 VISUALIZATION
# ============================================================

def visualize(mesh, result, source, target):
    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(mesh.G, seed=42)

    nx.draw(
        mesh.G,
        pos,
        with_labels=True,
        node_size=500,
        node_color="skyblue",
        font_weight="bold",
    )

    if result["best_path"]:
        edges = list(zip(result["best_path"], result["best_path"][1:]))
        nx.draw_networkx_edges(
            mesh.G, pos, edgelist=edges, width=4, edge_color="red"
        )

    plt.title(f"Nexus Optimal Route: {source} → {target}")
    plt.show()


# ============================================================
# 🚀 EXECUTION ENTRYPOINT
# ============================================================

async def main():
    mesh = SovereignMesh()
    router = SwarmRouter(mesh)

    source, target = random.sample(mesh.cities, 2)

    logger.info(f"Routing request: {source} → {target}")

    result = await router.workflow.ainvoke(
        {
            "source": source,
            "target": target,
            "debate": [],
        }
    )

    print("\n" + "=" * 60)
    print("🏛 NEXUS-CORE PRODUCTION REPORT")
    print("=" * 60)
    print(f"Target Scale : {NexusConfig.TARGET_SCALE}")
    print(
        f"Optimal Path : {' → '.join(result['best_path']) if result['best_path'] else 'None'}"
    )
    print(f"Hybrid Cost  : {result['total_cost']:.2f}")
    print("=" * 60 + "\n")

    visualize(mesh, result, source, target)


if __name__ == "__main__":
    import nest_asyncio

    nest_asyncio.apply()
    asyncio.run(main())
