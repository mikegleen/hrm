import csv
import json

f = open('/Users/mlg/Documents/hrm/aa_new_website/notes/trello_2021-01-10.json')
csvf = open('tmp/trello.csv', 'w')
parsed = json.load(f)
cards = parsed['cards']
print(len(cards))
csvw = csv.writer(csvf, lineterminator='\n')
for card in cards:
    csvw.writerow([card['name'].strip('\r').replace('\n', ' '),
                   card['desc'].strip('\r').replace('\n', ' ')])
