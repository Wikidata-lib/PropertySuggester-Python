import unittest
import gzip

from pkg_resources import resource_filename
from nose.tools import eq_

from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest
from propertysuggester.parser import JsonReader
from propertysuggester.utils.datamodel import Claim, Snak, Entity


class JsonReaderTest(AbstractUniverseTest):

    def test_updated_dump(self):
        file_name = resource_filename(__name__, "Wikidata-Q15511.json.gz")
        with gzip.open(file_name, 'r') as f:
            result = list(JsonReader.read_json(f))

        claim = Claim(
            Snak(1082, "quantity", "+25"),
            [
                Snak(585, "time", "+00000002001-01-01T00:00:00Z"),
                Snak(459, "wikibase-item", "Q745221")
            ],
            [Snak(248, "wikibase-item", "Q17597573")]
        )
        eq_(1, len(result))
        q15511 = result[0]
        eq_('Q15511', q15511.title)
        self.assertIn(claim, q15511.claims)

    def test_special_cases(self):
        data = dict([("id", "Q1"), ("type", "item")])
        eq_(Entity("Q1", []), JsonReader._process_json(data))


if __name__ == '__main__':
    unittest.main()
