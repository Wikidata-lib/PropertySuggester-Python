from StringIO import StringIO
import gzip
from pkg_resources import resource_filename

from testtools import TestCase
from testtools.matchers import Equals

from propertysuggester.parser import XmlReader
from propertysuggester.parser import CsvWriter
from propertysuggester.utils.datamodel import Entity, Claim, Snak

test_data = [Entity('Q51', [Claim(Snak(31, 'wikibase-entityid', 'Q5107')),
                            Claim(Snak(373, 'string', 'Europe'),
                                  [Snak(1, 'string', 'qual')],
                                  [Snak(2, 'string', 'ref')])])]


class CsvWriterTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_write_csv(self):
        out = StringIO()
        CsvWriter.write_csv(test_data, out)
        out.seek(0)

        line = out.readline()
        self.assertThat(line.strip(), Equals("Q51,claim,31,wikibase-entityid,Q5107"))

        line = out.readline()
        self.assertThat(line.strip(), Equals("Q51,claim,373,string,Europe"))

        line = out.readline()
        self.assertThat(line.strip(), Equals("Q51,qualifier,1,string,qual"))

        line = out.readline()
        self.assertThat(line.strip(), Equals("Q51,reference,2,string,ref"))

        self.assertThat(out.read(), Equals(""))

    def test_write_big_csv(self):
        out = StringIO()
        f = resource_filename(__name__, "Wikidata-20131129161111.xml.gz")
        xml = XmlReader.read_xml(gzip.open(f))
        CsvWriter.write_csv(xml, out)

        out.seek(0)
        self.assertThat(len(out.readlines()), Equals(5627))
