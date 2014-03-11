import sys
import time
import argparse

from propertysuggester.utils.CompressedFileType import CompressedFileType
from propertysuggester.utils.datatypes import Entity
from propertysuggester.parser import XmlReader


def write_csv(entities, output_file, sep=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type sep: str
    """
    s = u"{1}{0}{2}{0}{3}{0}{4}\n"
    for entity in entities:
        for claim in entity.claims:
            line = s.format(sep, entity.title, claim.property_id, claim.datatype, claim.value).encode("utf-8")
            output_file.write(line)

