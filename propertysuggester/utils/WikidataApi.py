import collections
import requests


class WikidataApi:
    def __init__(self, url):
        self.url = url

    def wbs_getsuggestions(self, entity=None, properties=None, limit=10, cont=0, language='en', search=''):
        """
        @type entity: str or None
        @type properties: collections.Iterable[int] or None
        @type limit: int
        @type cont: int
        @type language: str
        @type search: str
        @rtype : dict
        """
        if (entity and properties) or (not entity and not properties):
            raise AttributeError("provide either a entity or properties")

        params = {'action': 'wbsgetsuggestions',
                  'format': 'json',
                  'limit': limit,
                  'continue': cont,
                  'language': language,
                  'search': search}

        if entity:
            params['entity'] = entity
        elif properties:
            params['properties'] = ','.join(map(str, properties))

        result = requests.get(self.url, params=params)
        return self._check_response_status(result)

    def _check_response_status(self, response):
        """
        @type response: requests.Response
        @rtype : dict the Json response
        """
        if response.status_code != 200:
            raise Exception("invalid response", response, response.text)

        json_response = response.json()
        if "success" not in json_response or json_response["success"] != 1:
            errormsg = ""
            if "error" in json_response:
                errormsg += str(json_response["error"])
            raise Exception("api call failed", response, errormsg)

        return json_response