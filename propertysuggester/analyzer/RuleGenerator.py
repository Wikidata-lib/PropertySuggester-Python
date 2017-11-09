try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

import os
import logging
import itertools
from propertysuggester.analyzer.impl.MainAnalyzer import ItemAnalyzer
from propertysuggester.analyzer.impl.QualifierReferenceAnalyzer import (
    QualifierAnalyzer, ReferenceAnalyzer)

config = ConfigParser.ConfigParser()
config.read(
    os.path.join(
        os.path.abspath(
            os.path.dirname(__file__)),
        'analyzer.ini'))
classifying_pids = config.get(
    "mainAnalyzer",
    "classifying_properties").split(",")
classifying_pids = [int(i) for i in classifying_pids]


def compute_rules(entities, min_probability=0.01):
    """
    @type entities: collections.Iterable[Entity]
    @return: list[Rule]
    """

    analyzers = [
        ItemAnalyzer(classifying_pids),
        QualifierAnalyzer(),
        ReferenceAnalyzer()]

    for i, entity in enumerate(entities):
        if i % 100000 == 0 and i > 0:
            logging.info("processed {0} entities".format(i))
        for analyzer in analyzers:
            analyzer.process(entity)

    rules = filter(
        lambda rule: rule.probability > min_probability,
        itertools.chain(*(a.get_rules() for a in analyzers)))
    return rules
