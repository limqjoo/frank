import csv
import json

csvfile = open('script.csv', 'r')
jsonfile = open('script.json', 'w')

# script = csv.reader(csvfile, delimiter=',', quotechar='|')
fieldnames = ("character","type","delay","text")
reader = csv.DictReader(csvfile, fieldnames)
jsonfile.write('[\n')
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write(',\n')
jsonfile.write('\n]')
