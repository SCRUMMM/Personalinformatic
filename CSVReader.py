"""CSVReader for CM12005 coursework by Borre Luijken 2024-04-19

Reads the CSV and stores the data in several dictionaries:
 1. alcohol  = {Date : Alcohol Consumption (count)}
 2. asleep   = {Date : Sleep Analysis Asleep (hr)}
 3. in_bed   = {Date : Sleep Analysis In Bed (hr)}
 4. core     = {Date : Sleep Analysis Core (hr)}
 5. deep     = {Date : Sleep Analysis Deep (hr)}
 6. rem      = {Date : Sleep Analysis REM (hr)}
 7. awake    = {Date : Sleep Analysis Awake (hr)}
 8. acore    = {Alcohol Consumption (count) : [Sleep Analysis Core (hr)]}
 9. adeep    = {Alcohol Consumption (count) : [Sleep Analysis Deep (hr)]}
10. arem     = {Alcohol Consumption (count) : [Sleep Analysis REM (hr)]}
11. aawake   = {Alcohol Consumption (count) : [Sleep Analysis Awake (hr)]}

Data is stored to 2 decimal places.


----- Example Usage -----

reader = CSVReader()
reader.read("C:/Documents/Data.csv")
print(reader.in_bed['2024-04-15 00:00:00'])  # >>> 9.39
print(reader.adeep[3.0])                     # >>> [7.84, 6.67, 8.90]
"""


import csv


class CSVReader:
    def __init__(self):
        self.alcohol = {}
        self.asleep = {}
        self.in_bed = {}
        self.core = {}
        self.deep = {}
        self.rem = {}
        self.awake = {}
        self.acore = {}
        self.adeep = {}
        self.arem = {}
        self.aawake = {}
        self.dicts = [self.alcohol, self.asleep, self.in_bed, self.core,
                      self.deep, self.rem, self.awake, self.acore,
                      self.adeep, self.arem, self.aawake]
    
    
    def read(self, filePath):
        """Reads the CSV and stores the data in the dictionaries"""
        with open(filePath, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                for i, dict in enumerate(self.dicts[:7], 1):
                    dict[str(row[0])] = round(float(row[i]), 2)
            for date in self.alcohol:
                for dict in self.dicts[7:]:
                    if self.alcohol[date] not in dict:
                        dict[self.alcohol[date]] = []
                    dict[self.alcohol[date]] += [dict[date]]

