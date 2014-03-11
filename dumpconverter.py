import argparse
import sys
import time

from propertysuggester.parser import XmlReader, CsvWriter
from propertysuggester.utils.CompressedFileType import CompressedFileType

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="this program converts wikidata XML dumps to CSV data.")
    parser.add_argument("input", help="The XML input file (a wikidata dump), gzip is supported",
                        type=CompressedFileType('r'))
    parser.add_argument("output", help="The CSV output file (default=sys.stdout)", default=sys.stdout, nargs='?',
                        type=CompressedFileType('w'))
    parser.add_argument("-p", "--processes", help="Number of processors to use (default 4)", type=int, default=4)
    args = parser.parse_args()

    start = time.time()
    CsvWriter.write_csv(XmlReader.read_xml(args.input, args.processes), args.output)
    print "total time: %.2fs" % (time.time() - start)
