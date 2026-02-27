import os
import logging

class NexusConfig:
    ENV = os.getenv("NEXUS_ENV", "PRODUCTION")
    NODE_COUNT = int(os.getenv("NODE_COUNT", 20))
    TARGET_SCALE = 1_000_000_000_000
    EDGE_PROBABILITY = 0.25
    LOG_LEVEL = logging.INFO
