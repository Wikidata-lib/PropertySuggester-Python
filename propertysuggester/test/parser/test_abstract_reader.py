from testtools import TestCase
from testtools.matchers import *

from propertysuggester.utils.datamodel import Claim, Entity, Snak


class AbstractUniverseTest(TestCase):
    def assert_universe(self, result):
        self.assertThat(result, HasLength(1))
        q1 = result[0]

        self.assertThat(q1.title, Equals("Q1"))
        self.assertThat(q1.claims, Contains(Claim(Snak(373, "string", "Universe"), [],
                                                  [Snak(143, "wikibase-entityid", "Q328")])))
        self.assertThat(q1.claims, Contains(Claim(Snak(31, "wikibase-entityid", "Q223557"))))
        self.assertThat(q1.claims, Contains(Claim(Snak(31, "wikibase-entityid", "Q1088088"))))
        self.assertThat(q1.claims, Contains(Claim(Snak(361, "wikibase-entityid", "Q3327819"),
                                                  [Snak(31, "wikibase-entityid", "Q41719")], [])))
