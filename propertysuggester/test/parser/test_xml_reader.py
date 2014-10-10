import unittest
import gzip

from pkg_resources import resource_filename
from testtools import TestCase
from testtools.matchers import *

from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest
from propertysuggester.parser import XmlReader
from propertysuggester.utils.datamodel import Claim, Snak, Entity


class XmlReaderTest(AbstractUniverseTest):
    def test_universe(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q1.xml.gz"), "r") as f:
            result = list(XmlReader.read_xml(f))
        self.assert_universe(result)

    def test_updated_dump(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q9351.xml.gz"), "r") as f:
            result = list(XmlReader.read_xml(f))

        self.assertThat(len(result), Equals(1))
        q9351 = result[0]
        self.assertThat(q9351.title, Equals("Q9351"))
        self.assertThat(q9351.claims, Contains(Claim(Snak(156, "wikibase-item", "Q1647331"))))
        self.assertThat(q9351.claims, Contains(Claim(Snak(1112, "quantity", "+25"))))

    def test_special_cases(self):
        self.assertThat(XmlReader._process_json(("Q1", "{}")), Equals(Entity("Q1", [])))
        self.assertThat(XmlReader._process_json(("Q1", '{"claims":[{"m":["value","","bad"], "refs":[],"q":[]}]}')),
                        Equals(Entity("Q1", [])))
        self.assertThat(XmlReader._process_json(("Q1", '{"claims":[{"m":["value","","unknown"], "refs":[],"q":[]}]}')),
                        Equals(Entity("Q1", [])))

class MultiprocessingBigTest(TestCase):
    def test_simple_multiprocessing(self):
        r1 = list(XmlReader.read_xml(gzip.open(resource_filename(__name__, "Wikidata-Q1.xml.gz")), 1))
        r4 = list(XmlReader.read_xml(gzip.open(resource_filename(__name__, "Wikidata-Q1.xml.gz")), 4))

        self.assertThat(r1, HasLength(1))
        self.assertThat(r4, Equals(r1))

    def test_multiprocessing(self):
        r1 = list(XmlReader.read_xml(gzip.open(resource_filename(__name__, "Wikidata-20131129161111.xml.gz")), 1))
        r4 = list(XmlReader.read_xml(gzip.open(resource_filename(__name__, "Wikidata-20131129161111.xml.gz")), 4))

        self.assertThat(r1, HasLength(87))
        self.assertThat(r4, Equals(r1))

if __name__ == '__main__':
    unittest.main()

