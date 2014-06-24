import unittest

from testtools import TestCase
from testtools.matchers import *

from propertysuggester.analyzer import TableGenerator
from propertysuggester.utils.datamodel import Entity, Claim, Snak


test_data1 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107')),
                             Claim(Snak(373, 'string', 'Africa'))]),
              Entity('Q16', [Claim(Snak(31, 'wikibase-entityid', 'Q384'))])]

test_data2 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107')),
                             Claim(Snak(373, 'string', 'Africa')),
                             Claim(Snak(373, 'string', 'Europe'))])]

test_data3 = [Entity('Q15', [Claim(Snak(31, 'wikibase-entityid', 'Q5107'),
                                   [Snak(12, 'wikibase-entityid', 'Q123'), Snak(13, 'string', 'qual')],
                                   [Snak(22, 'wikibase-entityid', 'Q345'), Snak(23, 'string', 'rel')])])]



class TableGeneratorTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def test_table_generator(self):
        table, _, _ = TableGenerator.compute_table(test_data1)
        self.assertThat(table, ContainsAll((31, 373)))

        self.assertThat(table[31]['appearances'], Equals(2))
        self.assertThat(table[31]['type'], Equals('wikibase-entityid'))
        self.assertThat(table[31][31], Equals(0))
        self.assertThat(table[31][373], Equals(1))

        self.assertThat(table[373]['appearances'], Equals(1))
        self.assertThat(table[373]['type'], Equals('string'))
        self.assertThat(table[373][373], Equals(0))
        self.assertThat(table[373][31], Equals(1))

    def test_table_with_multiple_occurance(self):
        table, _, _ = TableGenerator.compute_table(test_data2)

        self.assertThat(table[31]['appearances'], Equals(1))
        self.assertThat(table[31]['type'], Equals('wikibase-entityid'))
        self.assertThat(table[31][31], Equals(0))
        self.assertThat(table[31][373], Equals(1))

        self.assertThat(table[373]['appearances'], Equals(1))
        self.assertThat(table[373]['type'], Equals('string'))
        self.assertThat(table[373][373], Equals(0))
        self.assertThat(table[373][31], Equals(1))

    def test_table_with_qualifier_and_references(self):
        table, table_qual, table_ref = TableGenerator.compute_table(test_data3)

        self.assertThat(table_qual[31]['appearances'], Equals(1))
        self.assertThat(table_qual[31]['type'], Equals('wikibase-entityid'))
        self.assertThat(table_qual[31][31], Equals(0))
        self.assertThat(table_qual[31][12], Equals(1))
        self.assertThat(table_qual[31][13], Equals(1))

        self.assertThat(table_ref[31]['appearances'], Equals(1))
        self.assertThat(table_ref[31]['type'], Equals('wikibase-entityid'))
        self.assertThat(table_ref[31][31], Equals(0))
        self.assertThat(table_ref[31][22], Equals(1))
        self.assertThat(table_ref[31][23], Equals(1))

if __name__ == '__main__':
    unittest.main()
