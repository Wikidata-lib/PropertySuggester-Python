from collections import defaultdict
from propertysuggester.analyzer.impl.Analyzer import Analyzer
from propertysuggester.analyzer.rule import Rule

class ItemAnalyzer(Analyzer):
    def __init__(self, classiying_property_ids = [31,279]):
        Analyzer.__init__(self)
        self.classiying_pids = classiying_property_ids
        self.tuple_occurrences = defaultdict(int)
        self.pair_occurrences = defaultdict(lambda: defaultdict(int))
    
    def process(self, item):
        distinct_ids = set(claim.mainsnak.property_id for claim in item.claims)
        property_value_pairs = [(claim.mainsnak.property_id, claim.mainsnak.value) for claim in item.claims]
        self._count_occurrences(distinct_ids, property_value_pairs)

    def _count_occurrences(self, distinct_ids, property_value_pairs):
        for pid1 in distinct_ids:
            if pid1 in self.classiying_pids:
                continue
            currentTuple = (pid1, None)
            self.tuple_occurrences[currentTuple] += 1
            for pid2 in distinct_ids:
                if pid1 != pid2:
                    self.pair_occurrences[currentTuple][pid2] += 1

        for pid1, value in property_value_pairs:
            if pid1 in self.classiying_pids and value[1:].isdigit():
                self.tuple_occurrences[pid1, int(value[1:])] += 1
                for pid2 in distinct_ids:
                    if pid1 != pid2:
                        self.pair_occurrences[pid1, int(value[1:])][pid2] += 1

    def get_rules(self):
        rules = []
        for (pid1, value), row in self.pair_occurrences.iteritems():
            pid1count = self.tuple_occurrences[pid1, value]
            for pid2, paircount in row.iteritems():
                if paircount > 0:
                    probability = (paircount/float(pid1count))
                    rules.append(Rule(pid1, value, pid2, paircount, probability, "item"))
        return rules
