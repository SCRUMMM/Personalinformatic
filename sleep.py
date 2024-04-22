class sleep():

    def __init__(self):
        self.sleep_record = {}
    
    def record(self, date, sleepdata):
        #sleepdata is stored as an array
        self.sleep_record[date] = sleepdata

    def get_quantity(self, date):
        return self.sleep_record.get(date, 0)

    def get_all_records(self):
        return self.sleep_record

    def set_sleepdata(self, date, sleepdata):
        if date in self.sleep_record:
            self.sleep_record[date] = sleepdata
        else:
            print("No record found for the given date.")

    def delete_record(self, date):
        if date in self.sleep_record:
            del self.sleep_record[date]
        else:
            print("No record found for the given date.")
