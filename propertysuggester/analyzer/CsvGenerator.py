import csv


def create_pair_csv(table, table_qualifier, table_references, out, delimiter=","):
    """
    @type table: dict[int, dict]
    @type out: file or StringIO.StringIO
    @type delimiter: string
    """
    csv_writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    print "properties: {0}".format(len(table))

    csv_writer.writerow(("pid1", "qid1", "pid2", "count", "probability", "context"))

    _write_entries(table, csv_writer, "item")
    _write_entries(table_qualifier, csv_writer, "qualifier")
    _write_entries(table_references, csv_writer, "reference")


def _write_entries(table, csv_writer, context):
    print "Writing entries with context " + context
    rowcount = 0
    for pid1, row in table.iteritems():
        for pid2, value in row.iteritems():
            if pid1 != pid2 and isinstance(pid2, int) and value > 0:  # "appearances" is in the same table, ignore them
                probability = value/float(row["appearances"])
                csv_writer.writerow((pid1, '', pid2, value, probability, context))
                rowcount += 1
                if not rowcount % 1000:
                    print "rows {0}".format(rowcount)
