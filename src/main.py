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

if __name__ == "__main__":
    logger.init()
    logger.debug("Initialized")

    inference.init(config.MODEL_NAMES.split(","))

    tagger = preprocessing.ItemTagger()

    while (inference_result := inference.step())[0]:
        inference_result = inference_result[1]
        tagger.add_from_results(inference_result)

    # for obj in tagger.tagged_objects:
    #     if obj.effective_confidence() < 0.1:
    #         continue
    #     print(obj)

    inference.deinit()
    logger.deinit()
