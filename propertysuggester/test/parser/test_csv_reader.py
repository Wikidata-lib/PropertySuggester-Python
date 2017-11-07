import logging

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from propertysuggester.parser import CsvReader
from propertysuggester.utils.datamodel import Claim, Entity, Snak


class TestCsvReader():
    def test_universe(self):
        out = StringIO()
        out.writelines(["Q1,claim,373,string,Universe\n",
                        "Q1,reference,143,wikibase-item,Q328\n"
                        "Q1,claim,31,wikibase-item,Q223557\n",
                        "Q1,claim,31,wikibase-item,Q1088088\n",
                        "Q1,claim,361,wikibase-item,Q3327819\n",
                        "Q1,qualifier,31,wikibase-item,Q41719\n"])
        out.seek(0)
        result = list(CsvReader.read_csv(out))
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

    def test_multiple_entities(self):
        out = StringIO()
        out.writelines(["Q1,claim,373,string,Universe\n",
                        "Q2,claim,143,wikibase-item,Q328\n"])
        out.seek(0)
        result = list(CsvReader.read_csv(out))

        assert 2 == len(result)
        assert 'Q1' == result[0].title
        assert 'Q2' == result[1].title

    def test_unknown_type(self):
        out = StringIO()
        out.writelines(["Q1,unknown,373,string,Universe\n"])
        out.seek(0)

        logging.basicConfig(level=40)  # Errors up to 30 (WARNING) are expected

        result = list(CsvReader.read_csv(out))
        assert 'Q1' == result[0].title

    def test_invalid_row_is_skipped(self):
        f = StringIO()
        f.writelines(["a,b"])
        f.seek(0)

        logging.basicConfig(level=40)  # Errors up to 30 (WARNING) are expected

        assert [] == list(CsvReader.read_csv(f))

    def test_tostring(self):
        e = Entity("Q1", [Claim(Snak(2, "string", "a"))])
        str(e)
