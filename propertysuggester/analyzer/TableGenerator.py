
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

    get_snak = lambda claim: claim.mainsnak

    for i, entity in enumerate(entities):
        if i % 100000 == 0 and i > 0:
            print "entities {0}".format(i)

        _get_property_types(entity, get_snak, table)
        distinct_ids = set(get_snak(claim).property_id for claim in entity.claims)
        _count_occurances(distinct_ids, table)

    return table, table_qua, table_ref


def _get_property_types(entity, get_snak, table):
    """
    @type entity: Entity
    @type table: dict[int, dict]
    """
    for claim in entity.claims:
        snak = get_snak(claim)
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
