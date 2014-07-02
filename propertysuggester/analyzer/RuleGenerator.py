from collections import defaultdict
import itertools
from propertysuggester.analyzer.rule import Rule
from propertysuggester.utils.datamodel import Entity


def compute_rules(entities):
    """
    @type entities: collections.Iterable[Entity]
    @return: list[Rule]
    """

    analyzers = [ItemAnalyzer(), QualifierAnalyzer(), ReferenceAnalyzer()]

    for i, entity in enumerate(entities):
        if i % 100000 == 0 and i > 0:
            print "entities {0}".format(i)
        for analyzer in analyzers:
            analyzer.process(entity)

    rules = itertools.chain(*(a.get_rules() for a in analyzers))
    return rules


class Analyzer:
    def __init__(self, context):
        """
        @type context: string
        """
        self.propertyOccurances = defaultdict(int)
        self.coOccurances = defaultdict(lambda: defaultdict(int))
        self.context = context

    def process(self, entity):
        """
        @type entity: Entity
        """
        raise NotImplemented("Please implement this method")

    def get_rules(self):
        """
        @return: list[Rule]
        """
        rules = []
        for pid1, row in self.coOccurances.iteritems():
            pid1count = self.propertyOccurances[pid1]
            for pid2, value in row.iteritems():
                if value > 0:
                    probability = value/float(pid1count)
                    rules.append(Rule(pid1, None, pid2, pid1count, probability, self.context))
        return rules


class ItemAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self, "item")

    def process(self, entity):
        distinct_ids = set(claim.mainsnak.property_id for claim in entity.claims)
        self._count_occurances(distinct_ids)

    def _count_occurances(self, distinct_ids):
        for pid1 in distinct_ids:
            self.propertyOccurances[pid1] += 1
            for pid2 in distinct_ids:
                if pid1 != pid2:
                    self.coOccurances[pid1][pid2] += 1


class QualifierAnalyzer(Analyzer):
    def __init__(self):
        Analyzer.__init__(self, "qualifier")

    def process(self, entity):
        for claim in entity.claims:
            distinct_pids = set(q.property_id for q in self.get_special(claim))
            if len(distinct_pids) > 0:
                self.propertyOccurances[claim.mainsnak.property_id] += 1
                self._count_special_appearances(claim.mainsnak.property_id, distinct_pids)

    def _count_special_appearances(self, mainsnak_id, distinct_ids):
        for pid in distinct_ids:
            self.coOccurances[mainsnak_id][pid] += 1

    def get_special(self, claim):
        return claim.qualifiers


class ReferenceAnalyzer(QualifierAnalyzer):
    def __init__(self):
        Analyzer.__init__(self, "reference")

    def get_special(self, claim):
        return claim.references
