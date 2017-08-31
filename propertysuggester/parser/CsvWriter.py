import csv
import logging


def write_csv(entities, output_file, delimiter=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type delimiter: str
    """
    csv_writer = csv.writer(output_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    for entity in entities:
        for claim in entity.claims:
            title = entity.title.encode("utf-8")
            write_row(csv_writer, title, "claim", claim.mainsnak)
            for q in claim.qualifiers:
                write_row(csv_writer, title, "qualifier", q)
            for ref in claim.references:
                write_row(csv_writer, title, "reference", ref)


def write_row(csv_writer, title, typ, snak):
    """
    @param csv_writer:
    @param snak: Snak
    @return:
    """
    try:
        row = (title, typ, snak.property_id, snak.datatype.encode("utf-8"), snak.value.encode("utf-8"))
    except AttributeError:
        logging.warning("attribute error, skip writing %s" % title)
        row = None

    if row is not None:
        csv_writer.writerow(row)
