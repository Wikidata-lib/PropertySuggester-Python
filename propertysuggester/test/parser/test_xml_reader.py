import unittest
import gzip

from pkg_resources import resource_filename
from unittest import TestCase
from nose.tools import eq_

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

        eq_(1, len(result))
        q9351 = result[0]
        eq_('Q9351', q9351.title)
        self.assertIn(Claim(Snak(156, "wikibase-item", "Q1647331")),
                      q9351.claims)
        self.assertIn(Claim(Snak(1112, "quantity", "+25")), q9351.claims)

    def test_special_cases(self):
        eq_(Entity("Q1", []), XmlReader._process_json(("Q1", "{}")))
        data = '{"claims":[{"m":["value","","bad"], "refs":[],"q":[]}]}'
        eq_(Entity("Q1", []), XmlReader._process_json(("Q1", data)))
        data = '{"claims":[{"m":["value","","unknown"], "refs":[],"q":[]}]}'
        eq_(Entity("Q1", []), XmlReader._process_json(("Q1", data)))


class MultiprocessingBigTest(TestCase):
    def test_simple_multiprocessing(self):
        r1 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, "Wikidata-Q1.xml.gz")), 1))
        r4 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, "Wikidata-Q1.xml.gz")), 4))

        eq_(1, len(r1))
        eq_(r1, r4)

    def test_multiprocessing(self):
        file_name = "Wikidata-20131129161111.xml.gz"
        r1 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, file_name)), 1))
        r4 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, file_name)), 4))

        eq_(87, len(r1))
        eq_(r1, r4)


if __name__ == '__main__':
    unittest.main()
