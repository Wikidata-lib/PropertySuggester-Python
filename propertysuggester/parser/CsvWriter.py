import csv
import logging
import sys


def compatible_str(term):
    # TODO: Remove this when migrated to python3
    if isinstance(term, str):
        return term
    if sys.version_info < (3,):
        return str(term.encode('utf-8'))
    else:
        return str(term, 'utf-8')


def write_csv(entities, output_file, delimiter=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type delimiter: str
    """
    csv_writer = csv.writer(
        output_file,
        delimiter=delimiter,
        quoting=csv.QUOTE_MINIMAL)

    for entity in entities:
        for claim in entity.claims:
            title = entity.title.encode("utf-8")
            write_row(csv_writer, title, "claim", claim.mainsnak)
            for q in claim.qualifiers:
                write_row(csv_writer, title, "qualifier", q)
            for ref in claim.references:
                write_row(csv_writer, title, "reference", ref)


def write_row(csv_writer, title, type_, snak):
    """
    @param csv_writer:
    @param snak: Snak
    @return:
    """
    try:
        row = (compatible_str(title), type_, snak.property_id,
               compatible_str(snak.datatype), compatible_str(snak.value))
    except AttributeError:
        logging.warning("attribute error, skip writing %s" % title)
        row = None

    if row is not None:
        csv_writer.writerow(row)
