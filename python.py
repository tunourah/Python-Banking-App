import csv

with open('bank.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file , delimiter=';')
    for line in csv_reader:

      print(line)
