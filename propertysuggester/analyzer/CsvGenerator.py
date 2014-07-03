import csv
from propertysuggester.analyzer.rule import Rule


def create_pair_csv(rules, out, delimiter=","):
    """
    @type rules: list[Rule]
    @type out: file or StringIO.StringIO
    @type delimiter: string
    """
    csv_writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')

    csv_writer.writerow(("pid1", "qid1", "pid2", "count", "probability", "context"))
    rowcount = 0
    for rule in rules:
        csv_writer.writerow((rule.pid1, rule.qid1 or '', rule.pid2, rule.count, rule.probability, rule.context))
        rowcount += 1
        if rowcount % 1000 == 0:
            print "rows {0}".format(rowcount)
