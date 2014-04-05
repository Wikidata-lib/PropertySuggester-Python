from StringIO import StringIO
import unittest

from testtools import TestCase
from testtools.matchers import Equals

from propertysuggester.analyzer import CsvGenerator


class SqlGeneratorTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.file = StringIO()

    def test_create_table(self):
        table = {1: {'appearances': 8, 'type': 'string', 2: 5, 3: 0}}
        CsvGenerator.create_pair_csv(table, self.file)

        self.file.seek(0)
        self.assertThat(self.file.readline().strip(), Equals("pid1;pid2;count;probability"))
        prob = 5.0 / 8.0
        self.assertThat(self.file.readline().strip(), Equals("1;2;5;{0}".format(prob)))


if __name__ == '__main__':
    unittest.main()