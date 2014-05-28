import cPickle as pickle

def write_csv(entities, output_file, delimiter=","):
    """
    @type entities: collections.Iterable[Entity]
    @type output_file: file or StringIO.StringIO
    @type delimiter: str
    """

    for entity in entities:
        pickle.dump(entity, output_file, protocol=2)
