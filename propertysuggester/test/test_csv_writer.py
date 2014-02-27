from StringIO import StringIO
import gzip
from  pkg_resources import resource_filename

import unittest
from testtools import TestCase
from testtools.matchers import *

from propertysuggester.parser import XmlReader
from propertysuggester.parser import CsvWriter
from propertysuggester.utils.datatypes import Entity, Claim

test_data = [Entity('Q51', [Claim(31, 'wikibase-entityid', 'Q5107'),
                            Claim(373, 'string', 'Europe')])]


class CsvWriterTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)


    def testWriteCsv(self):
        out = StringIO()
        CsvWriter.write_csv(test_data, out)
        out.seek(0)

        line = out.readline()
        self.assertThat(line, Equals("Q51,31,wikibase-entityid,Q5107\n"))

        line = out.readline()
        self.assertThat(line, Equals("Q51,373,string,Europe\n"))

        self.assertThat(out.read(), Equals(""))

    def testWriteBigCsv(self):
        out = StringIO()
        f = resource_filename("propertysuggester.test", "Wikidata-20131129161111.xml.gz")
        xml = XmlReader.read_xml(gzip.open(f))
        CsvWriter.write_csv(xml, out)

        out.seek(0)
        self.assertThat(len(out.readlines()), Equals(3679))


if __name__ == '__main__':
    unittest.main()

