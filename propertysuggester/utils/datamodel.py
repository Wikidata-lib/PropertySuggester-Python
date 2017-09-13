class Entity:
    def __init__(self, name, claims):
        """
        @type name: str
        @type claims: list[Claim]
        """
        self.title = name
        self.claims = claims

    def __eq__(self, other):
        return isinstance(other, Entity) and self.__dict__ == other.__dict__

    def __repr__(self):
        return "title: {0} claims: {1}".format(self.title, map(str, self.claims))


class Claim:
    def __init__(self, mainsnak, qualifiers=None, references=None):
        """
        @type mainsnak: Snak
        @type qualifiers: list[Snak]
        @type references: list[Snak]
        """
        self.mainsnak = mainsnak
        self.qualifiers = qualifiers or []
        self.references = references or []

    def __eq__(self, other):
        return isinstance(other, Claim) and self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)


class Snak:
    def __init__(self, property_id, datatype, value):
        """
        @type property_id: int
        @type datatype: string
        @type value: string
        """
        self.property_id = property_id
        self.datatype = datatype
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Snak) and self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)
