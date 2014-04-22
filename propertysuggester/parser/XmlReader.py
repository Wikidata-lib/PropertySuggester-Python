"""
read_xml returns a generator that yields Entities)

usage:
with open("file.csv", "r") as f:
    for entity in read_xml(f):
        do_things()

"""
import multiprocessing
import traceback
import signal
from propertysuggester.utils.datamodel import Claim, Entity

try:
    import ujson as json
except ImportError:
    print "ujson not found"
    import json as json

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    print "cElementTree not found"
    import xml.etree.ElementTree as ElementTree


NS = "http://www.mediawiki.org/xml/export-0.8/"
title_tag = "{" + NS + "}" + "title"
text_tag = "{" + NS + "}" + "text"
model_tag = "{" + NS + "}" + "model"
page_tag = "{" + NS + "}" + "page"


# http://noswap.com/blog/python-multiprocessing-keyboardinterrupt
def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def read_xml(input_file, thread_count=1):
    """
    @rtype : collections.Iterable[Entity]
    @type input_file:  file or GzipFile or StringIO.StringIO
    @type thread_count: int
    """
    if thread_count > 1:
        # thread_count -1 because one thread is for xml parsing
        pool = multiprocessing.Pool(thread_count - 1, init_worker)
        try:
            for entity in pool.imap(_process_json, _get_xml(input_file)):
                yield entity
        except KeyboardInterrupt:
            print "KeyboardInterrupt"
            pool.terminate()
        except Exception:
            pool.terminate()
            traceback.format_exc()
        else:
            pool.close()
        finally:
            pool.join()
    else:
        for title, claim_json in _get_xml(input_file):
            yield _process_json((title, claim_json))


def _get_xml(input_file):
    count = 0
    title = claim_json = model = None
    for event, element in ElementTree.iterparse(input_file):
        if element.tag == title_tag:
            title = element.text
        elif element.tag == model_tag:
            model = element.text
        elif element.tag == text_tag:
            claim_json = element.text
        elif element.tag == page_tag:
            count += 1
            if count % 3000 == 0:
                print "processed %.2fMB" % (input_file.tell() / 1024.0 ** 2)
            if model == "wikibase-item":
                yield title, claim_json
        element.clear()


def _process_json((title, json_string)):
    data = json.loads(json_string)
    if not "claims" in data:
        return Entity(title, [])

    claims = []
    for claim in data["claims"]:
        claim = claim["m"]
        property_id = claim[1]
        if claim[0] == "value":
            datatype = claim[2]
            if datatype == "string":
                value = claim[3]
            elif datatype == "wikibase-entityid":
                value = "Q" + str(claim[3]["numeric-id"])
            elif datatype == "time":
                value = claim[3]["time"]
            elif datatype == "quantity":
                value = claim[3]["amount"]
            elif datatype == "globecoordinate":
                value = "N{0}, E{1}".format(claim[3]["latitude"], claim[3]["longitude"])
            elif datatype == "bad":
                # for example in Q2241
                continue
            else:
                print "WARNING unknown wikidata datatype: %s" % datatype
                continue
        else:  # novalue, somevalue, ...
            datatype = "unknown"
            value = claim[0]

        claims.append(Claim(property_id, datatype, value))
    return Entity(title, claims)

