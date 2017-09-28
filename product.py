from datetime import datetime

class Product():
    def __init__(self, cost, name, date):
        self.cost = cost
        self.name = name
        self.date = date

    def days_left(self):
        return datetime.now() - self.date
