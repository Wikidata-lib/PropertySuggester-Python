from collections import defaultdict
from propertysuggester.utils.datamodel import Entity


def compute_table(entities):
    """
    @type entities: collections.Iterable[Entity]
    @return: dict[int, dict]
    """
    table = defaultdict(lambda: defaultdict(int))
    table_qua = defaultdict(lambda: defaultdict(int))
    table_ref = defaultdict(lambda: defaultdict(int))

    for i, entity in enumerate(entities):
        if i % 100000 == 0 and i > 0:
            print "entities {0}".format(i)

        _get_property_types(entity, table)
        distinct_ids = set(claim.mainsnak.property_id for claim in entity.claims)
        _count_occurances(distinct_ids, table)

        for claim in entity.claims:
            _count_special_appearances(claim, lambda c: c.qualifier, table_qua)
            _count_special_appearances(claim, lambda c: c.references, table_ref)

    return table, table_qua, table_ref


def _get_property_types(entity, table):
    """
    @type entity: Entity
    @type table: dict[int, dict]
    """
    for claim in entity.claims:
        snak = claim.mainsnak
        if not snak.property_id in table or table[snak.property_id]["type"] == "unknown":
            table[snak.property_id]["type"] = snak.datatype


def _count_occurances(distinct_ids, table):
    """
    @type distinct_ids: set[int]
    @type table: dict[int, dict]
    """
    for pid1 in distinct_ids:
        table[pid1]["appearances"] += 1
        for pid2 in distinct_ids:
            if pid1 != pid2:
                table[pid1][pid2] += 1


def _count_special_appearances(claim, get_special, special_table):
    """
    @type claim: Claim
    @type special_table: dict[int,dict]
    """
    if len(claim.qualifier) > 0:
        snak = claim.mainsnak
        if not snak.property_id in special_table:
            special_table[snak.property_id]["type"] = snak.datatype
        special_table[snak.property_id]["appearances"] += 1
        for q in get_special(claim):
            special_table[snak.property_id][q.property_id] += 1
