

class Analyzer:
    def __init__(self):
        pass

    def process(self, entity):
        """
        @type entity: Entity
        """
        raise NotImplementedError("Please implement this method")

    def get_rules(self):
        """
        @return: list[Rule]
        """
        raise NotImplementedError("Please implement this method")
