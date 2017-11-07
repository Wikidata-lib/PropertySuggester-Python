try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from propertysuggester.analyzer import CsvGenerator
from propertysuggester.analyzer.rule import Rule


class TestCsvGenerator():
    def test_create_table(self):
        file_ = StringIO()
        rule = Rule(1, None, 2, 5, 0.3, "item")
        CsvGenerator.create_pair_csv([rule], file_)

        file_.seek(0)
        assert ('pid1,qid1,pid2,count,probability,context' ==
                file_.readline().strip())
        assert '1,,2,5,0.3,item' == file_.readline().strip()
