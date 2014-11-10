import unittest
import gzip

from pkg_resources import resource_filename
from testtools import TestCase
from testtools.matchers import *

from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest
from propertysuggester.parser import JsonReader
from propertysuggester.utils.datamodel import Claim, Snak, Entity


class JsonReaderTest(AbstractUniverseTest):

    def test_updated_dump(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q15511.json.gz"), "r") as f:
            result = list(JsonReader.read_json(f))

        self.assertThat(result, HasLength(1))
        q15511 = result[0]
        self.assertThat(q15511.title, Equals("Q15511"))
        self.assertThat(q15511.claims, Contains(Claim(Snak(1082, "quantity", "+25"), [Snak(585, "time", "+00000002001-01-01T00:00:00Z"), Snak(459, "wikibase-item", "Q745221")], [Snak(248, "wikibase-item", "Q17597573")])))

    def test_special_cases(self):
        data = dict([("id", "Q1"), ("type", "item")])
        self.assertThat(JsonReader._process_json(data), Equals(Entity("Q1", [])))

if __name__ == '__main__':
    unittest.main()
    