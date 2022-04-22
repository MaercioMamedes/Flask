import csv
import json
import shelve


def read_database(*ticker):

    with shelve.open('database') as db:
        dictionary = dict(db)
    return dictionary[ticker[0]] if len(ticker) > 0 else dictionary


def write_database(ticker, long_name):
    with shelve.open('database') as db:
        db[ticker] = long_name




