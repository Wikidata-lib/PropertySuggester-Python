"""
read_csv returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in read_csv(f):
        do_things()

"""
import cPickle as pickle

def read_csv(input_file, delimiter=","):
    """
    @rtype : collections.Iterable[Entity]
    @type input_file: file or StringIO.StringIO
    @type delimiter: str
    """

    while True:
        try:
            yield pickle.load(input_file)
        except EOFError:
            break

    return
