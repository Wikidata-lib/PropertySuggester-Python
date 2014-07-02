import unittest

from testtools import TestCase
from testtools.matchers import *

from propertysuggester.analyzer import RuleGenerator
from propertysuggester.analyzer.rule import Rule
from propertysuggester.utils.datamodel import Entity, Claim, Snak


test_data1 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107')),
                             Claim(Snak(373, 'string', 'Africa'))]),
              Entity('Q16', [Claim(Snak(31, 'wikibase-entityid', 'Q384'))])]

test_data2 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107')),
                             Claim(Snak(373, 'string', 'Africa')),
                             Claim(Snak(373, 'string', 'Europe'))])]

test_data3 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107'),
                                   [Snak(12, 'wikibase-entityid', 'Q123'), Snak(13, 'string', 'qual')],
                                   [Snak(22, 'wikibase-entityid', 'Q345'), Snak(23, 'string', 'rel')])])]


class RuleGeneratorTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_table_generator(self):
        rules = list(RuleGenerator.compute_rules(test_data1))
        self.assertThat(rules, ContainsAll([Rule(31, None, 373, 2, 0.5, "item"), Rule(373, None, 31, 1, 1.0, "item")]))


    def test_table_with_multiple_occurance(self):
        rules = list(RuleGenerator.compute_rules(test_data2))
        self.assertThat(rules, ContainsAll([Rule(31, None, 373, 1, 1.0, "item"), Rule(373, None, 31, 1, 1.0, "item")]))

    def test_table_with_qualifier_and_references(self):
        rules = list(RuleGenerator.compute_rules(test_data3))
        self.assertThat(rules, ContainsAll([Rule(31, None, 12, 1, 1.0, "qualifier"),
                                            Rule(31, None, 13, 1, 1.0, "qualifier"),
                                            Rule(31, None, 22, 1, 1.0, "reference"),
                                            Rule(31, None, 23, 1, 1.0, "reference")]))


if __name__ == '__main__':
    unittest.main()
