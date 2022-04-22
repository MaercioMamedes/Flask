import csv
import shelve
import json
import os

with shelve.open('database') as db:
    with open(os.path.join('static/js/data.json'), 'w') as file:
        content = dict(db)
        file.write(json.dumps(content))
