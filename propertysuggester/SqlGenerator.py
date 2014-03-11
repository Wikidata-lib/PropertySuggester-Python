from MySQLdb.cursors import Cursor


def load_table_into_db(table, db):
    """

    @type table: dict[int, dict]
    @type db: Cursor
    """
    db.execute("CREATE TABLE IF NOT EXISTS wbs_properties(pid INT, count INT, type varchar(20), primary key(pid))")
    db.execute("CREATE TABLE IF NOT EXISTS wbs_propertyPairs(pid1 INT, pid2 INT, count INT, probability FLOAT, primary key(pid1, pid2))")
    db.execute("DELETE FROM wbs_propertyPairs")
    db.execute("DELETE FROM wbs_properties")

    print "properties: {0}".format(len(table))
    rowcount = 0
    for pid1, row in table.iteritems():
        db.execute("INSERT INTO wbs_properties(pid, count, type) VALUES (%s, %s, %s)", (pid1, row["appearances"], row["type"]))
        for pid2, value in row.iteritems():
            if pid1 != pid2 and isinstance(pid2, int) and value > 0:  # "appearances" and "type" is in the same table, ignore them
                probability = value/float(row["appearances"])
                db.execute("INSERT INTO wbs_propertyPairs(pid1, pid2, count, probability) VALUES (%s, %s, %s, %s)", (pid1, pid2, value, probability))
                rowcount += 1
                if not rowcount % 1000:
                    print "rows {0}".format(rowcount)



