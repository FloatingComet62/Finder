"""
a. Main entry point to the project
b. Logic to
I. Initialise the system
II. Load input source
III. Call inference pipeline
IV. Display and output
"""

import logger
import inference

if __name__ == "__main__":
    logger.init()
    logger.debug("Init")

    inference.init("yolov8s.pt")

    while inference.step():
        pass

    inference.deinit()
    logger.deinit()
