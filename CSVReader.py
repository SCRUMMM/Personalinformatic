"""CSVReader for CM12005 coursework by Borre Luijken 2024-04-15

Assumed CSV format: date, alcohol quantity, sleep hours, sleep quality

Reads the CSV and stores the data in 3 dictionaries:
1. alcohol  = {date : alcohol quantity}
2. hours    = {date : sleep hours}
3. quality  = {date : sleep quality}


----- Example Usage -----

reader = CSVReader()
reader.read("C:/Documents/ExampleCSV")
print(reader.quality['2024-04-15'])  # >>> "good"
"""


import csv


class CSVReader:
    
    alchol = {}
    hours = {}
    quality = {}
    
    def __init__(self):
        self.alcohol = {}
        self.hours = {}
        self.quality = {}
    
    def read(self, filePath):
        """Reads the CSV and puts the data in the dictionaries"""
        with open(filePath, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.alcohol[row[0]] = row[1]
                self.hours[row[0]] = row[2]
                self.qualiy[row[0]] = row[3]

