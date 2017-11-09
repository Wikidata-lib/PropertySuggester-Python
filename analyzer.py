import logging
import argparse
import sys
import time

from propertysuggester.analyzer import CsvGenerator, RuleGenerator
from propertysuggester.parser import CsvReader
from propertysuggester.utils.CompressedFileType import CompressedFileType

if __name__ == "__main__":
    logging.basicConfig(level=20)  # Print logging.info

    parser = argparse.ArgumentParser(
        description="this program generates a correlation-table from "
                    "the csv-dump")
    parser.add_argument("input", help="The CSV input file (wikidata triple)",
                        type=CompressedFileType('rb'))
    parser.add_argument("output",
                        help="The CSV output file (default=sys.stdout)",
                        default=sys.stdout, nargs='?',
                        type=CompressedFileType('wb'))
    args = parser.parse_args()

    start = time.time()
    logging.info("computing table")
    rules = RuleGenerator.compute_rules(CsvReader.read_csv(args.input))
    logging.info("writing csv")
    CsvGenerator.create_pair_csv(rules, args.output)
    logging.info("done - {0:.2f}s".format(time.time() - start))
    logging.info("now import this csv file with "
                 "PropertySuggester/maintenance/UpdateTable.php")
