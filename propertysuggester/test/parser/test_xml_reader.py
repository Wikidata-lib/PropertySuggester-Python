import unittest
import gzip

from pkg_resources import resource_filename
from testtools import TestCase
from testtools.matchers import *

from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest
from propertysuggester.parser import XmlReader
from propertysuggester.utils.datamodel import Claim


class XmlReaderTest(AbstractUniverseTest):
    def setUp(self):
        TestCase.setUp(self)
        with gzip.open(resource_filename(__name__, "Wikidata-Q1.xml.gz"), "r") as f:
            self.result = list(XmlReader.read_xml(f))

    def test_updated_dump(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q9351.xml.gz"), "r") as f:
            result = list(XmlReader.read_xml(f))

        self.assertThat(len(result), Equals(1))
        q9351 = result[0]
        self.assertThat(q9351.title, Equals("Q9351"))
        self.assertThat(q9351.claims, Contains(Claim(156, "wikibase-entityid", "Q1647331")))
        self.assertThat(q9351.claims, Contains(Claim(1112, "quantity", "+25")))


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

