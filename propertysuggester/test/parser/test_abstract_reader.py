from unittest import TestCase
from nose.tools import eq_

from propertysuggester.utils.datamodel import Claim, Snak


class AbstractUniverseTest(TestCase):
    def assert_universe(self, result):
        eq_(1, len(result))
        q1 = result[0]

        eq_("Q1", q1.title)
        self.assertIn(Claim(Snak(373, "string", "Universe"), [],
                            [Snak(143, "wikibase-item", "Q328")]),
                      q1.claims)
        self.assertIn(Claim(Snak(31, "wikibase-item", "Q223557")), q1.claims)
        self.assertIn(Claim(Snak(31, "wikibase-item", "Q1088088")), q1.claims)
        self.assertIn(Claim(Snak(361, "wikibase-item", "Q3327819"),
                            [Snak(31, "wikibase-item", "Q41719")], []),
                      q1.claims)
