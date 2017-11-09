"""
read_csv returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in read_csv(f):
        do_things()

"""
import logging
import csv

from propertysuggester.utils.datamodel import Claim, Entity, Snak


def read_csv(input_file, delimiter=","):
    """
    @rtype : collections.Iterable[Entity]
    @type input_file: file or StringIO.StringIO
    @type delimiter: str
    """
    current_title = None
    current_claim = None
    claims = []
    csv_reader = csv.reader(
        input_file,
        delimiter=delimiter,
        quoting=csv.QUOTE_MINIMAL)

    for row in csv_reader:
        if len(row) != 5:
            logging.warning("error: {0}".format(row))
            continue
        title, typ, property_id, datatype, value = row
        if current_title != title:
            if current_title is not None:
                yield Entity(current_title, claims)
            current_title = title
            claims = []
        snak = Snak(int(property_id), datatype, value)
        if typ == 'claim':
            current_claim = Claim(snak)
            claims.append(current_claim)
        elif typ == 'reference':
            current_claim.references.append(snak)
        elif typ == 'qualifier':
            current_claim.qualifiers.append(snak)
        else:
            logging.warning("unknown type: {0}".format(typ))

    if current_title is not None:
        yield Entity(current_title, claims)
