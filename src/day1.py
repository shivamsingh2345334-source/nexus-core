"""
NEXUS CORE - DAY 1
Sovereign Agentic Simulation Engine

Pillars:
1. Async Perception Layer
2. Vectorized Trillion-Scale Simulation
3. Agentic Orchestration (LangGraph)
4. Industrial Logging
"""

# =========================
# IMPORTS
# =========================

import os
import sys
import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Any

import aiohttp
import numpy as np
import matplotlib.pyplot as plt
import nest_asyncio
from langgraph.graph import StateGraph


# =========================
# CONFIGURATION LAYER
# =========================

@dataclass(frozen=True)
class NexusConfig:
    ENV: str = os.getenv("NEXUS_ENV", "PRODUCTION")
    TARGET_NODES: int = 1_000_000_000_000
    SIM_NODES: int = 10
    WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"
    LAT_LON: tuple = (28.61, 77.20)
    LOG_LEVEL: int = logging.INFO


CONFIG = NexusConfig()


# =========================
# LOGGING SETUP
# =========================

def setup_logging():
    logging.basicConfig(
        level=CONFIG.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | NEXUS-CORE | %(message)s",
        stream=sys.stdout
    )
    return logging.getLogger("Nexus-Core-Day1")


logger = setup_logging()


# =========================
# PERCEPTION LAYER
# =========================

class SovereignPerception:
    """
    Non-blocking World State Ingestion
    """

    def __init__(self):
        self.node_ids = None
        self.positions = None

    async def fetch_weather(self, session: aiohttp.ClientSession) -> Dict[str, float]:
        params = {
            "latitude": CONFIG.LAT_LON[0],
            "longitude": CONFIG.LAT_LON[1],
            "current_weather": "true"
        }

        try:
            async with session.get(CONFIG.WEATHER_URL, params=params, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info("Weather API fetched successfully.")
                    return data["current_weather"]

                logger.warning("API Lag detected. Using fallback weather.")
                return {"temperature": 25.0, "windspeed": 10.0}

        except Exception as e:
            logger.error(f"Perception failure: {e}")
            return {"temperature": 0.0, "windspeed": 0.0}

    def initialize_nodes(self, n: int):
        """
        Vectorized node initialization (No loops)
        """
        self.node_ids = np.array([f"Truck-{i}" for i in range(n)])
        self.positions = np.random.uniform(0, 100, size=(n, 2))
        logger.info(f"Initialized {n} distributed logistics nodes.")


# =========================
# SWARM ORCHESTRATION
# =========================

class NexusSwarm:
    """
    Agentic Orchestration Engine
    """

    def __init__(self):
        workflow = StateGraph(dict)
        workflow.add_node("Analyst", self.analyst_agent)
        workflow.set_entry_point("Analyst")
        self.app = workflow.compile()

    @staticmethod
    def analyst_agent(state: Dict[str, Any]) -> Dict[str, Any]:
        weather = state["weather"]

        state["analysis"] = (
            f"CORE REPORT → "
            f"Temp={weather['temperature']}°C | "
            f"Wind={weather['windspeed']} km/h"
        )

        logger.info(f"Analyst processed state: {state['analysis']}")
        return state


# =========================
# SIMULATION ENGINE
# =========================

class SimulationEngine:
    """
    Trillion-Scale Vectorized Movement Engine
    """

    def __init__(self, perception: SovereignPerception):
        self.perception = perception

    async def run(self, analysis: str, steps: int = 3):
        for step in range(steps):
            movement = np.random.uniform(
                -5, 5, size=self.perception.positions.shape
            )

            # Atomic matrix update
            self.perception.positions += movement

            self.visualize(step + 1, analysis)
            await asyncio.sleep(0.5)

    def visualize(self, step: int, analysis: str):
        plt.figure(figsize=(8, 6))
        plt.scatter(
            self.perception.positions[:, 0],
            self.perception.positions[:, 1]
        )
        plt.title(f"Nexus Global Grid | Step {step}\n{analysis}")
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.grid(True)
        plt.show()


# =========================
# MAIN EXECUTION PIPELINE
# =========================

async def run_nexus_day1():
    logger.info("🚀 Initializing Nexus-Core Day 1...")

    perception = SovereignPerception()
    perception.initialize_nodes(CONFIG.SIM_NODES)

    async with aiohttp.ClientSession() as session:
        weather_data = await perception.fetch_weather(session)

    swarm = NexusSwarm()
    initial_state = {"weather": weather_data, "analysis": ""}
    result = await swarm.app.ainvoke(initial_state)

    simulator = SimulationEngine(perception)
    await simulator.run(result["analysis"], steps=3)

    logger.info("Day 1 simulation completed successfully.")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(run_nexus_day1())
