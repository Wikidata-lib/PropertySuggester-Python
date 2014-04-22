from StringIO import StringIO

from testtools import TestCase

from propertysuggester.parser import CsvReader
from propertysuggester.test.parser.test_abstract_reader import AbstractUniverseTest


class CsvReaderTest(AbstractUniverseTest):
    def setUp(self):
        TestCase.setUp(self)
        out = StringIO()
        out.writelines(["Q1,373,string,Universe\n",
                        "Q1,31,wikibase-entityid,Q223557\n",
                        "Q1,31,wikibase-entityid,Q1088088\n"])
        out.seek(0)
        self.result = list(CsvReader.read_csv(out))


class CsvReaderTest2(AbstractUniverseTest):
    def testInvalidRowThrowsException(self):
        f = StringIO()
        f.writelines(["a,b"])
        f.seek(0)

        self.assertRaises(ValueError, lambda: list(CsvReader.read_csv(f)))
