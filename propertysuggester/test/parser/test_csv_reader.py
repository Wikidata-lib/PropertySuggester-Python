from StringIO import StringIO

from testtools import TestCase
from testtools.matchers import *

from propertysuggester.parser import CsvReader
from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest
from propertysuggester.utils.datamodel import Claim, Entity, Snak


class CsvReaderTest(AbstractUniverseTest):
    def setUp(self):
        AbstractUniverseTest.setUp(self)


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
        self.assert_universe(result)

    def test_multiple_entities(self):
        out = StringIO()
        out.writelines(["Q1,claim,373,string,Universe\n",
                        "Q2,claim,143,wikibase-item,Q328\n"])
        out.seek(0)
        result = list(CsvReader.read_csv(out))

        self.assertThat(result, HasLength(2))
        self.assertThat(result[0].title, Equals("Q1"))
        self.assertThat(result[1].title, Equals("Q2"))

    def test_unknown_type(self):
        out = StringIO()
        out.writelines(["Q1,unknown,373,string,Universe\n"])
        out.seek(0)
        result = list(CsvReader.read_csv(out))

    def test_invalid_row_throws_exception(self):
        f = StringIO()
        f.writelines(["a,b"])
        f.seek(0)
        self.assertRaises(ValueError, lambda: list(CsvReader.read_csv(f)))

    def test_tostring(self):
        e = Entity("Q1", [Claim(Snak(2,"string","a"))])
        str(e)
