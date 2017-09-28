from datetime import datetime
from enum import Enum
import csv


class Phase(Enum):
    TROQ = 1


class Product():
    def __init__(self, cost, name, date, id_, passed_phases=None):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = passed_phases or set()
        self.id_ = id_

    def days_left(self):
        return self.date - datetime.now()

    def import_csv(path):
        products = []
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for idx, row in enumerate(reader):
                products.append(
                    Product(
                        id_=idx,
                        cost={key: int(value) for (key, value) in
                              zip(range(1, 14), row["Costo"].split(","))},
                        name=row['Producto'],
                        date=datetime.strptime(row['Fecha'], '%d/%m/%Y'),
                        passed_phases={int(x) for x in
                                       row["Fases Pasadas"].split(",")}))
        return products


def main():
    products = None
    best = {'vector': random_permutation(products)}


if __name__ == '__main__':
    main()


def random_permutation(products):
    pass
