"""
a. Main entry point to the project
b. Logic to
I. Initialise the system
II. Load input source
III. Call inference pipeline
IV. Display and output
"""
import logger

if __name__ == "__main__":
    logger.init()
    logger.debug("Init")
    logger.deinit()
