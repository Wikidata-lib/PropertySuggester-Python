from collections import defaultdict
import math
from propertysuggester.analyzer.impl.Analyzer import Analyzer
from propertysuggester.analyzer.rule import Rule


class ItemAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.propertyOccurances = defaultdict(int)
        self.coOccurances = defaultdict(lambda: defaultdict(int))
    
    def process(self, entity):
        distinct_ids = set(claim.mainsnak.property_id for claim in entity.claims)
        self._count_occurances(distinct_ids)

    def _count_occurances(self, distinct_ids):
        for pid1 in distinct_ids:
            self.propertyOccurances[pid1] += 1
            for pid2 in distinct_ids:
                if pid1 != pid2:
                    self.coOccurances[pid1][pid2] += 1

    def get_rules(self):
        rules = []
        totalpropertycount = len(self.propertyOccurances)
        for pid1, row in self.coOccurances.iteritems():
            sharedpids = len(row)
            idf = math.log(totalpropertycount/float(sharedpids))
            pid1count = self.propertyOccurances[pid1]
            for pid2, paircount in row.iteritems():
                if paircount > 0:
                    probability = (paircount/float(pid1count)) * idf
                    rules.append(Rule(pid1, None, pid2, paircount, probability, "item"))
        return rules