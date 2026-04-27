"""
a. Main entry point to the project
b. Logic to
I. Initialise the system
II. Load input source
III. Call inference pipeline
IV. Display and output
"""

import config
import logger
import inference
import preprocessing
import processing

if __name__ == "__main__":
    logger.init(file=open("stdout.log", "w"))
    logger.debug("Initialized")

    inference.init(config.MODEL_NAMES)

    tagger = preprocessing.ItemTagger()
    ownerships = processing.ItemOwnershipProcessor()

    while (inference_result := inference.step())[0]:
        inference_result = inference_result[1]
        tagger.add_from_results(inference_result)

    inference.deinit()
    logger.deinit()
