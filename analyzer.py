import argparse
import sys
import time

from propertysuggester import MatrixGenerator, CsvGenerator
from propertysuggester.parser import CsvReader
from propertysuggester.utils.CompressedFileType import CompressedFileType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="this program generates a correlation-table from the csv-dump")
    parser.add_argument("input", help="The CSV input file (wikidata triple)", type=CompressedFileType('r'))
    parser.add_argument("output", help="The CSV output file (default=sys.stdout)", default=sys.stdout, nargs='?',
                        type=CompressedFileType('wb'))
    args = parser.parse_args()

    start = time.time()
    print "computing table"
    t = MatrixGenerator.compute_table(CsvReader.read_csv(args.input))
    print "done - {0:.2f}s".format(time.time()-start)
    print "writing to database"
    CsvGenerator.create_pair_csv(t, args.output)