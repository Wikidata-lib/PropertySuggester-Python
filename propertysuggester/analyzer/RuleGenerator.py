from collections import defaultdict
import itertools
from propertysuggester.analyzer.impl.MainAnalyzer import ItemAnalyzer
from propertysuggester.analyzer.impl.QualifierReferenceAnalyzer import QualifierAnalyzer, ReferenceAnalyzer
from propertysuggester.analyzer.rule import Rule
from propertysuggester.utils.datamodel import Entity


def compute_rules(entities, min_probability=0.01):
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

    rules = filter(lambda rule: rule.probability > min_probability, itertools.chain(*(a.get_rules() for a in analyzers)))
    return rules

