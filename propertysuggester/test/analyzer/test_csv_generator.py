try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import unittest

from unittest import TestCase
from nose.tools import eq_

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
        eq_('pid1,qid1,pid2,count,probability,context',
            self.file.readline().strip())
        eq_('1,,2,5,0.3,item', self.file.readline().strip())


if __name__ == '__main__':
    unittest.main()
