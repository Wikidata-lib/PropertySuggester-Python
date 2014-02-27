import argparse
from datetime import time
import MySQLdb

from propertysuggester import MatrixGenerator, SqlGenerator
from propertysuggester.parser import CsvReader
from propertysuggester.utils.CompressedFileType import CompressedFileType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="this program generates a correlation-table from a CSV-file")
    parser.add_argument("input", help="The CSV input file (wikidata triple)", type=CompressedFileType('r'))
    parser.add_argument("db", help="target database")
    parser.add_argument("--host", help="DB host", default="127.0.0.1")
    parser.add_argument("--user", help="username for DB", default="root")
    parser.add_argument("--pw", help="pw for DB", default="")
    args = parser.parse_args()

    connection = MySQLdb.connect(host=args.host, user=args.user, passwd=args.pw, db=args.db)
    cursor = connection.cursor()
    start = time.time()
    print "computing table"
    t = MatrixGenerator.compute_table(CsvReader.read_csv(args.input))
    print "done - {0:.2f}s".format(time.time()-start)
    print "writing to database"
    SqlGenerator.load_table_into_db(t, cursor)
    cursor.close()
    connection.commit()
