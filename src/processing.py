from logger import ModuleLogger

logger = ModuleLogger("Processing")

INITIAL_CONFIDENCE = 0.1
TICK_CONFIDENCE = 0.02
PARENT_PROXIMITY = 100
PARENT_CLASSNAMES = ["Person", "Man", "Woman", "Human face"]


def filter_parents(objects):
    parents = []
    not_parents = []
    for obj in objects:
        if obj.name in PARENT_CLASSNAMES:
            parents.append(obj)
        else:
            not_parents.append(obj)
    return parents, not_parents


class Ownership:
    def __init__(self, self_item, parent):
        s = f"{self_item.name}({self_item.id})"
        p = f"{parent.name}({parent.id})"
        logger.debug(f"Assuming ownership of {s} by {p}")
        self.item = self_item
        self.parent = parent
        self.confidence = INITIAL_CONFIDENCE

    def tick_positive_confidence(self):
        self.confidence += TICK_CONFIDENCE
        o = f"{self.item.id} by {self.parent.id}"
        c = f"{self.confidence}"
        logger.debug(f"Ownership confidence of {o} increased to {c}")

    def tick_negative_confidence(self):
        self.confidence = max(self.confidence - TICK_CONFIDENCE, 0)
        o = f"{self.item.id} by {self.parent.id}"
        c = f"{self.confidence}"
        logger.debug(f"Ownership confidence of {o} decreased to {c}")

    def tick(self, proximity):
        if proximity:
            self.tick_positive_confidence()
        else:
            self.tick_negative_confidence()


class ItemOwnershipProcessor:
    def __init__(self):
        self.ownerships = {}

    def tick(self, objects):
        parents, not_parents = filter_parents(objects)
        for parent in parents:
            for not_parent in not_parents:
                if self.ownerships.get(parent) is None:
                    self.ownerships[parent] = {}

                if self.ownerships[parent].get(not_parent) is None:
                    self.ownerships[parent][not_parent] = Ownership(
                        not_parent, parent
                    )

                distance = (parent.position - not_parent.position).dist()
                proximity = 1 if distance < PARENT_PROXIMITY else 0
                self.ownerships[parent][not_parent].tick(proximity)
