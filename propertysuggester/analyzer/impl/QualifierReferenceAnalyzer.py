from collections import defaultdict
from propertysuggester.analyzer.impl.Analyzer import Analyzer
from propertysuggester.analyzer.rule import Rule


class QualifierAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self)
        self.main_occurances = defaultdict(int)
        self.qualifier_occurances = defaultdict(lambda: defaultdict(int))
        self.context = "qualifier"

    def process(self, entity):
        for claim in entity.claims:
            distinct_pids = set(q.property_id for q in self.get_special(claim))
            if len(distinct_pids) > 0:
                main_pid = claim.mainsnak.property_id
                self.main_occurances[main_pid] += 1
                self._count_special_appearances(main_pid, distinct_pids)

    def _count_special_appearances(self, mainsnak_id, distinct_ids):
        for pid in distinct_ids:
            self.qualifier_occurances[mainsnak_id][pid] += 1

    def get_special(self, claim):
        return claim.qualifiers

    def get_rules(self):
        rules = []
        for main_pid, row in self.qualifier_occurances.items():
            maincount = self.main_occurances[main_pid]
            for qualifier_pid, paircount in row.items():
                if paircount > 0:
                    probability = paircount/float(maincount)
                    rules.append(Rule(main_pid, None, qualifier_pid, paircount,
                                      probability, self.context))
        return rules


class ReferenceAnalyzer(QualifierAnalyzer):
    def __init__(self):
        QualifierAnalyzer.__init__(self)
        self.context = "reference"

    def get_special(self, claim):
        return claim.references
