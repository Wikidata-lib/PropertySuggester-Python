"""
process_json returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in process_json(f):
        do_things()

"""
from propertysuggester.utils.datamodel import Claim, Entity, Snak

try:
    import ujson as json
except ImportError:
    print "ujson not found"
    import json as json

def process_json(input_file):
    count = 0
    for jsonline in input_file:
        count += 1 
        if count % 3000 == 0:
            print "processed %.2fMB" % (input_file.tell() / 1024.0 ** 2)
        jsonline = jsonline[:-2]
        try:
            data = json.loads(jsonline)
        except ValueError:
            continue
        if data["type"] == "item":
            title = data["id"]
            if not "claims" in data:
                yield Entity(title, [])
                continue
            claims = []
            for prop, statements in data["claims"].iteritems():
                for statement in statements:
                    references = []
                    if "references" in statement:
                        for prop, snaks in statement["references"][0]["snaks"].iteritems():
                            for snak in snaks:
                                ref = _parse_json_snak(snak)
                                if ref:
                                    references.append(ref)
                    qualifiers = []
                    if "qualifiers" in statement:                            
                        for prop, snaks in statement["qualifiers"].iteritems():
                            for snak in snaks: 
                                qualifier = _parse_json_snak(snak)
                            if qualifier:
                                qualifiers.append(qualifier)
                    claim = _parse_json_snak(statement["mainsnak"])
                    if claim:
                        claims.append(Claim(claim, qualifiers, references))

            yield Entity(title, claims)


def _parse_json_snak(claim_json):
    if claim_json["snaktype"] == "value":
        datatype = claim_json["datatype"]
        datavalue = claim_json["datavalue"]["value"]
        if datatype == "string":
            value = datavalue
        elif datatype == "wikibase-item":
            if datavalue["entity-type"] == "item":
                value = "Q" + str(datavalue["numeric-id"])
            else:
                print "WARNING unknown entitytype: {0}".format(datavalue["entity-type"])
        elif datatype == "time":
            value = datavalue["time"]
        elif datatype == "quantity":
            value = datavalue["amount"]
        elif datatype == "globe-coordinate":
            value = "N{0}, E{1}".format(datavalue["latitude"], datavalue["longitude"])
        elif datatype == "bad":
            # for example in Q2241
            return None
        else:
            #print "WARNING unknown wikidata datatype: %s" % datatype
            value = "irrelevant"
    else:  # novalue, somevalue, ...
        datatype = "unknown"
        value = claim_json["snaktype"]
    property_id = claim_json["property"][1:]
    return Snak(property_id, datatype, value)
