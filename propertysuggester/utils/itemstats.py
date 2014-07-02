from collections import defaultdict
from propertysuggester.parser import CsvReader

reader = CsvReader.read_csv(file(r"C:\repos\PropertySuggester-Python\wikidatawiki-20140526-pages-articles.csv"), ",")

itemcount = 0
statementcount = 0

for i, item in enumerate(reader):
    itemcount += 1
    statementcount += len(item.claims)

    if i > 0 and i % 100000 == 0:
        print i,
    if i % (100000 * 10) == 0:
        print

print
print "items:", itemcount
print "statements:", statementcount
