

class AlcoholConsumption():
    def __init__(self):
        self.consumption_record = {}

    def record(self, date, quantity):
        self.consumption_record[date] = quantity

    def get_quantity(self, date):
        return self.consumption_record.get(date, 0)

    def get_all_records(self):
        return self.consumption_record

    def set_quantity(self, date, quantity):
        if date in self.consumption_record:
            self.consumption_record[date] = quantity
        else:
            print("No record found for the given date.")

    def delete_record(self, date):
        if date in self.consumption_record:
            del self.consumption_record[date]
        else:
            print("No record found for the given date.")

# Example usage:
alcohol = AlcoholConsumption()

# Record alcohol consumption for a date
alcohol.record("2024-04-15", 2)

# Get alcohol consumption for a specific date
print(alcohol.get_quantity("2024-04-15"))  # Output: 2

# Get all consumption records
print(alcohol.get_all_records())  # Output: {'2024-04-15': 2}

# Update alcohol consumption for a date
alcohol.set_quantity("2024-04-15", 3)

# Get updated alcohol consumption for the date
print(alcohol.get_quantity("2024-04-15"))  # Output: 3

# Delete a consumption record
alcohol.delete_record("2024-04-15")

# Get all consumption records after deletion
print(alcohol.get_all_records())  # Output: {}
