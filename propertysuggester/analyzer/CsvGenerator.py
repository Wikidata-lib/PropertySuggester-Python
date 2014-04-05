import csv


def create_pair_csv(table, out, delimiter=";"):
    """
    @type table: dict[int, dict]
    @type out: file or StringIO.StringIO
    @type delimiter: string
    """
    csv_writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
    print "properties: {0}".format(len(table))

    csv_writer.writerow(("pid1", "pid2", "count", "probability"))
    rowcount = 0
    for pid1, row in table.iteritems():
        for pid2, value in row.iteritems():
            if pid1 != pid2 and isinstance(pid2, int) and value > 0:  # "appearances" is in the same table, ignore them
                probability = value/float(row["appearances"])
                csv_writer.writerow((pid1, pid2, value, probability))
                rowcount += 1
                if not rowcount % 1000:
                    print "rows {0}".format(rowcount)
