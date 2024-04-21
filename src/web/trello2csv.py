import csv
import json

f = open('/Users/mlg/pyprj/hrm/data/trello/2023-10-20_trello.json')
csvf = open('tmp/trello.csv', 'w')
parsed = json.load(f)
cards = parsed['cards']
print(len(cards))
csvw = csv.writer(csvf, lineterminator='\n')
for card in cards:
    csvw.writerow([card['name'].strip('\r').replace('\n', ' '),
                   card['desc'].strip('\r').replace('\n', ' ')])
