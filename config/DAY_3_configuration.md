# ⚙️ Nexus Neural Core – Configuration Guide (DAY-3)

The system is driven by a centralized configuration



---

## 📌 Core Configuration

```python
import logging

NEXUS_CONFIG = {
    "LEARNING_RATE": 0.03,
    "WEIGHT_BOUNDS": (0.1, 0.9),
    "NODE_COUNT": 20,
    "LOG_LEVEL": logging.INFO
}
