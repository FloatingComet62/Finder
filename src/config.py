"""
a. Configuration file
b. Must include
I. Model path
II. Input source
III. Thresholds / parameters
IV. Log file path
"""

from dotenv import load_dotenv
import os

load_dotenv()

LEVELS = {
    "DEBUG": 3,
    "INFO": 2,
    "WARN": 1,
    "ERROR": 0,
}
LOG_LEVEL = LEVELS.get(
    (os.environ.get("LOG_LEVEL") or "").upper()
) or LEVELS["ERROR"]
MODEL_NAMES = os.environ["MODEL_NAMES"]
