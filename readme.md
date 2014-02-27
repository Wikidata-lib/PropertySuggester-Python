# PropertySuggester-Python
Contains scripts for PropertySuggester to preprocess the wikidata dump

## usage 
- use dumpconverter.py to convert a wikidata dump to csv
- use sqlloader.py to load suggestion data from csv into the wikidata db


### install
```
sudo apt-get install build-essential libmysqlclient-dev python-pip python-dev
pip install -r requirements.txt
```

### run tests
```
nosetests
```

[![Build Status](https://travis-ci.org/Wikidata-lib/PropertySuggester-Python.png?branch=master)](https://travis-ci.org/Wikidata-lib/PropertySuggester-Python)
