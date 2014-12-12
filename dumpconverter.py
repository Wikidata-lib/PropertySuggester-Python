import logging
import argparse
import sys
import time

from propertysuggester.parser import JsonReader, CsvWriter
from propertysuggester.utils.CompressedFileType import CompressedFileType

if __name__ == "__main__":
    logging.basicConfig(level=20) # Print logging.info

    parser = argparse.ArgumentParser(description="this program converts wikidata JSON dumps to CSV data.")
    parser.add_argument("input", help="The JSON input file (a wikidata dump)", type=CompressedFileType('r'))
    parser.add_argument("output", help="The CSV output file (default=sys.stdout)", default=sys.stdout, nargs='?',
                        type=CompressedFileType('wb'))
    #parser.add_argument("-p", "--processes", help="Number of processors to use (default 4)", type=int, default=4)
    args = parser.parse_args()
    start = time.time()
    CsvWriter.write_csv(JsonReader.read_json(args.input), args.output)
    logging.info("total time: %.2fs" % (time.time() - start))
