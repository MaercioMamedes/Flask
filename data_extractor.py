import csv
import json


def read_csv(*ticker):
    dictionary = {}
    with open('b3.csv', 'r') as file:
        content = csv.reader(file)
        for x in content:
            dictionary[x[0]] = x[1]

    return dictionary[ticker[0]] if len(ticker) > 0 else dictionary


def write_csv(ticker, long_name):
    with open('b3.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((ticker[:-3], long_name))




