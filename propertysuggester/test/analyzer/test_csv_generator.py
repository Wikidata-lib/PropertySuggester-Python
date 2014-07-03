from StringIO import StringIO
import unittest

from testtools import TestCase
from testtools.matchers import Equals

from propertysuggester.analyzer import CsvGenerator
from propertysuggester.analyzer.rule import Rule


class CsvGeneratorTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.file = StringIO()

    def test_create_table(self):
        rule = Rule(1, None, 2, 5, 0.3, "item")
        CsvGenerator.create_pair_csv([rule], self.file)

        self.file.seek(0)
        self.assertThat(self.file.readline().strip(), Equals("pid1,qid1,pid2,count,probability,context"))
        self.assertThat(self.file.readline().strip(), Equals("1,,2,5,0.3,item"))


if __name__ == '__main__':
    unittest.main()
