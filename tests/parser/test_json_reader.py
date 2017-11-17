import gzip

from pkg_resources import resource_filename

from propertysuggester.parser import JsonReader
from propertysuggester.utils.datamodel import Claim, Snak, Entity


class TestJsonReader():
    def test_updated_dump(self):
        file_name = resource_filename(__name__, "Wikidata-Q15511.json.gz")
        with gzip.open(file_name, 'r') as f:
            result = list(JsonReader.read_json(f))

        claim = Claim(
            Snak(1082, "quantity", "+25"),
            [
                Snak(459, "wikibase-item", "Q745221"),
                Snak(585, "time", "+00000002001-01-01T00:00:00Z")
            ],
            [Snak(248, "wikibase-item", "Q17597573")]
        )
        assert 1 == len(result)
        q15511 = result[0]
        assert 'Q15511' == q15511.title
        assert claim in q15511.claims

    def test_special_cases(self):
        data = dict([("id", "Q1"), ("type", "item")])
        assert Entity("Q1", []) == JsonReader._process_json(data)
