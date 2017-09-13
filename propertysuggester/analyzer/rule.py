
class Rule:

    def __init__(self, pid1, qid1, pid2, count, probability, context):
        """
        @type pid1: int
        @type qid1: int|None
        @type pid2: int
        @type count: int
        @type probability: float
        @type context: string
        """
        self.pid1 = pid1
        self.qid1 = qid1
        self.pid2 = pid2
        self.count = count
        self.probability = probability
        self.context = context

    def __eq__(self, other):
        return isinstance(other, Rule) and self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)
