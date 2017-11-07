import gzip

from pkg_resources import resource_filename

from propertysuggester.parser import XmlReader
from propertysuggester.utils.datamodel import Claim, Snak, Entity


class TestXmlReader():
    def test_universe(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q1.xml.gz"), "r") as f:
            result = list(XmlReader.read_xml(f))
        assert 1 == len(result)
        q1 = result[0]

        assert "Q1" == q1.title
        assert (Claim(Snak(373, "string", "Universe"), [],
                [Snak(143, "wikibase-item", "Q328")]) in
                q1.claims)
        assert Claim(Snak(31, "wikibase-item", "Q223557")) in q1.claims
        assert Claim(Snak(31, "wikibase-item", "Q1088088")) in q1.claims
        assert (Claim(Snak(361, "wikibase-item", "Q3327819"),
                [Snak(31, "wikibase-item", "Q41719")], []) in
                q1.claims)

    def test_updated_dump(self):
        with gzip.open(resource_filename(__name__, "Wikidata-Q9351.xml.gz"), "r") as f:
            result = list(XmlReader.read_xml(f))

        assert 1 == len(result)
        q9351 = result[0]
        assert 'Q9351' == q9351.title
        assert (Claim(Snak(156, "wikibase-item", "Q1647331")) in
                q9351.claims)
        assert Claim(Snak(1112, "quantity", "+25")) in q9351.claims

    def test_special_cases(self):
        assert Entity("Q1", []) == XmlReader._process_json(("Q1", "{}"))
        data = '{"claims":[{"m":["value","","bad"], "refs":[],"q":[]}]}'
        assert Entity("Q1", []) == XmlReader._process_json(("Q1", data))
        data = '{"claims":[{"m":["value","","unknown"], "refs":[],"q":[]}]}'
        assert Entity("Q1", []) == XmlReader._process_json(("Q1", data))


class TestMultiprocessingBig():
    def test_simple_multiprocessing(self):
        r1 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, "Wikidata-Q1.xml.gz")), 1))
        r4 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, "Wikidata-Q1.xml.gz")), 4))

        assert 1 == len(r1)
        assert r1 == r4

    def test_multiprocessing(self):
        file_name = "Wikidata-20131129161111.xml.gz"
        r1 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, file_name)), 1))
        r4 = list(XmlReader.read_xml(gzip.open(
            resource_filename(__name__, file_name)), 4))

        assert 87 == len(r1)
        assert r1 == r4
