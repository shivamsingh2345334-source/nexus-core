"""
NEXUS CORE CONFIGURATION

Centralized configuration layer
for system parameters and scaling controls.
Author: Shivam Singh
"""

NEXUS_CONFIG = {

    # Batch processing size
    "BATCH_SIZE": 20,

    # Target simulation scale
    "SCALE_TARGET": 1_000_000_000_000,

    # CPU worker processes
    "WORKER_COUNT": 4,

    # External weather risk API
    "WEATHER_API_URL": "https://api.open-meteo.com/v1/forecast",

    # Geographic coordinates
    "LAT_LON": (28.61, 77.20),

    # Timeout control
    "API_TIMEOUT": 2,

    # Telemetry settings
    "ENABLE_TELEMETRY": True,

    # Visualization
    "ENABLE_VISUALIZATION": True

}
