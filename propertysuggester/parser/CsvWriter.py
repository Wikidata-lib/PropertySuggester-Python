import csv

from propertysuggester.utils.datamodel import Entity


def write_csv(entities, output_file, delimiter=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type delimiter: str
    """
    csv_writer = csv.writer(output_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    for entity in entities:
        for claim in entity.claims:
            row = (entity.title.encode("utf-8"), claim.property_id, claim.datatype.encode("utf-8"), claim.value.encode("utf-8"))
            csv_writer.writerow(row)

