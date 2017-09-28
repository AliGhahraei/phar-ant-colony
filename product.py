from datetime import datetime

class Product():
    def __init__(self, cost, name, date):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = set()

    def days_left(self):
        return datetime.now() - self.date


def main():
    products = None
    best = {'vector': random_permutation(products)}


if __name__ == '__main__':
    main()


def random_permutation(products):
    pass
