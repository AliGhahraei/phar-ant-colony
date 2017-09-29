from datetime import datetime
from enum import Enum
import csv

dependencies = {1: set(), 2: set(), 3: set(), 4: {1, 2, 3}, 5: {4}, 6: {4}, 7: {5, 6}, 8: [], 9: [8], 10: [9], 11: [],
                12: [], 13: [11, 12], 14: [13, 10, 7]}


class Product():
    def __init__(self, cost, name, date, passed_phases=None):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = passed_phases or set()

    def hours_left(self):
        hours = abs(self.date - datetime.now())
        return hours.total_seconds() / 3600

    def import_csv(path):
        products = []
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                products.append(
                    Product(
                        cost={key: int(value) for (key, value) in
                              zip(range(1, 14), row["Costo"].split(","))},
                        name=row['Producto'],
                        date=datetime.strptime(row['Fecha'], '%d/%m/%Y'),
                        passed_phases={int(x) for x in
                                       row["Fases Pasadas"].split(",")}))
        return products


# Calcula dependencia
def depCalc(root, prod):
    costAcum = 0
    if len(dependencies[root]) != 0:
        costAcum += depCalc(max(dependencies[root]), prod)
        return costAcum
    else:
        return prod.cost[root]


# Calcula paralelo
# Calcula el costo de un resultado de combinancion usando el numero de pedidos retrasados y tiempo total
# Que le toma realizar esa solucion
def cost(result):
    totalCost = 0
    delayed = 0
    for component in result:
        for product in result[component]:
            if product.hours_left() - product.cost[component] + depCalc(component, product) < 0:
                delayed += 1
            totalCost = totalCost + product.cost[component] + depCalc(component, product)
    # if(totalCost -
    return delayed * totalCost


def main():
    products = Product.import_csv("datos.csv")
    print(cost({4: products}))
    # products = None
    # best = {'vector': random_permutation(products)}


if __name__ == '__main__':
    main()


def random_permutation(products):
    pass
