"""
read_csv returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in read_csv(f):
        do_things()

"""

from propertysuggester.utils.datatypes import Claim, Entity

def read_csv(input_file, separator=","):
    """
    @rtype : collections.Iterable[Entity]
    @type input_file: file or StringIO.StringIO
    @type separator: str
    """
    current_title = None
    claims = []
    for line in input_file:
        title, prop, datatype, value = line.strip().split(separator, 3)
        if current_title != title:
            if not current_title is None:
                yield Entity(current_title, claims)
            current_title = title
            claims = []
        claims.append(Claim(int(prop), datatype, value))

    if not current_title is None:
        yield Entity(current_title, claims)

