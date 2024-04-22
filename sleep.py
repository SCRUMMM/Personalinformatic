class sleep():

    def __init__(self):
        self.sleep_record = {}
    
    def record(self, date, sleepdata):
        #sleepdata is stored as an array
        self.consumption_record[date] = sleepdata

    def get_quantity(self, date):
        return self.consumption_record.get(date, 0)

    def get_all_records(self):
        return self.consumption_record

    def set_sleepdata(self, date, sleepdata):
        if date in self.consumption_record:
            self.consumption_record[date] = sleepdata
        else:
            print("No record found for the given date.")

    def delete_record(self, date):
        if date in self.consumption_record:
            del self.consumption_record[date]
        else:
            print("No record found for the given date.")
