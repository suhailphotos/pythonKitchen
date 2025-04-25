import csv
import os

file_path = os.path.expanduser('~/.incept/mapping/lessons.csv')

with open(file_path, mode='r', encoding='utf-8-sig', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)

