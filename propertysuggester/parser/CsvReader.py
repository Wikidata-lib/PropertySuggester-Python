"""
read_csv returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in read_csv(f):
        do_things()

"""
import csv

from propertysuggester.utils.datatypes import Claim, Entity


def read_csv(input_file, delimiter=","):
    """
    @rtype : collections.Iterable[Entity]
    @type input_file: file or StringIO.StringIO
    @type delimiter: str
    """
    current_title = None
    claims = []
    csv_reader = csv.reader(input_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    for row in csv_reader:
        if len(row) != 4:
            print "error: {0}".format(row)
        title, prop, datatype, value = row
        if current_title != title:
            if not current_title is None:
                yield Entity(current_title, claims)
            current_title = title
            claims = []
        claims.append(Claim(int(prop), datatype, value))

    if not current_title is None:
        yield Entity(current_title, claims)

