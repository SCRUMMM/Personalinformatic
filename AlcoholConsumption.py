


class AlcoholConsumption():
    def __init__(self, quantity, date):
        self.quantity = quantity
        self.date = date
    
    def record(self):
        pass

    def get_quantity(self):
        return self.quantity
    
    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_date(self):
        return self.date
    
    def set_date(self, date):
        self.date = date
    