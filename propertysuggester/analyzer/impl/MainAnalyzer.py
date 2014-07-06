from collections import defaultdict
from propertysuggester.analyzer.impl.Analyzer import Analyzer
from propertysuggester.analyzer.rule import Rule

classiying_property_ids = [31,279]

class ItemAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.tuple_occurrences = defaultdict(int)
        self.pair_occurrences = defaultdict(lambda: defaultdict(int))
    
    def process(self, item):
        distinct_ids = set(claim.mainsnak.property_id for claim in entity.claims)
        property_value_pairs = claim.mainsnak.property_id, claim.mainsnak.value for claim in entity.claims
        self._count_occurrences(distinct_ids, property_value_pairs)

    def _count_occurrences(self, distinct_ids, property_value_pairs):
        for pid1 in distinct_ids:
            if pid1 in classiying_property_ids:
                continue
            currentTuple = (pid1, None)
            self.tuple_occurrences[currentTuple] += 1
            for pid2 in distinct_ids:
                if pid1 != pid2:
                    self.pair_occurrences[currentTuple][pid2] += 1

        for pid1, value in property_value_pairs:
            if pid in classiying_property_ids:
                self.tuple_occurrences[pid, value] += 1
                for pid2 in distinct_ids:
                    if pid1 != pid2:
                        self.pair_occurrences[pid1, value][pid2] += 1

    def get_rules(self):
        rules = []
        for pid1, row in self.pair_occurrences.iteritems():
            pid1count = self.property_occurrences[pid1]
            for pid2, paircount in row.iteritems():
                if paircount > 0:
                    probability = (paircount/float(pid1count))
                    rules.append(Rule(pid1, None, pid2, paircount, probability, "item"))
        return rules
