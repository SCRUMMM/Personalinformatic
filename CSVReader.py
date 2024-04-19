"""CSVReader for CM12005 coursework by Borre Luijken 2024-04-19

Assumed sleep CSV format: date, sleep hours, sleep quality
Assumed alcohol CSV format: date, alcohol quantity

Reads the CSVs and stores the data in 3 dictionaries:
1. alcohol  = {date : alcohol quantity}
2. hours    = {date : sleep hours}
3. quality  = {date : sleep quality}


----- Example Usage -----

reader = CSVReader()
reader.read("C:/Documents/ExampleSleepCSV", "C:/Documents/ExampleAlcoholCSV")
print(reader.quality['2024-04-15'])  # >>> "good"
"""


import csv


class CSVReader:
    def __init__(self):
        self.alcohol = {}
        self.hours = {}
        self.quality = {}
    
    
    def read(self, filePathSleep, filePathAlcohol):
        """Reads the CSVs and stores the data in the dictionaries"""
        with open(filePathSleep, 'r') as fs:
            reader = csv.reader(fs, delimiter=',')
            for row in reader:
                self.hours[row[0]] = row[1]
                self.quality[row[0]] = row[2]
        
        with open(filePathAlcohol, 'r') as fa:
            reader = csv.reader(fa, delimiter=',')
            for row in reader:
                self.alcohol[row[0]] = row[1]

