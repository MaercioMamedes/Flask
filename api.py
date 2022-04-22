from main import *
import shelve
import json


@app.route('/api')
def api():
    with shelve.open('database') as db_js:
        return json.dumps(dict(db_js))
