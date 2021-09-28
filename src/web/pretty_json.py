import json
f = open('/Users/mlg/Documents/hrm/aa_new_website/notes/trello_2021-01-10.json')
parsed = json.load(f)
print(json.dumps(parsed, indent=4, sort_keys=True))
