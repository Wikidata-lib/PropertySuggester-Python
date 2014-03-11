import csv

from propertysuggester.utils.datatypes import Entity

def write_csv(entities, output_file, delimiter=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type delimiter: str
    """
    csv_writer = csv.writer(output_file, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)

    for entity in entities:
        for claim in entity.claims:
            csv_writer.writerow((entity.title.encode("utf-8"), claim.property_id, claim.datatype, claim.value.encode("utf-8")))

