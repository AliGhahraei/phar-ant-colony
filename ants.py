from datetime import datetime
from enum import Enum
import csv

dependencies = {1:set(),2:set(),3:set(),4:{1,2,3},5:{4},6:{4},7:{5,6},8:[],9:[8],10:[9],11:[],12:[],13:[11,12],14:[13,10,7]}


class Product():
    def __init__(self, cost, name, date, id_, passed_phases=None):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = passed_phases or set()
        self.id_ = id_

    def days_left(self):
        return self.date.hours - datetime.now().hours()

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


def depCalc(root,prod):
    '''Calcula dependencia'''
    costAcum = 0
    if len(dependencies[root]) != 0:
        costAcum += depCalc(max(dependencies[root]),prod)
        return costAcum
    else:
        return prod.cost[root]

def cost(result):
    '''
    Calcula paralelo
    Calcula el costo de un resultado de combinancion usando el numero de pedidos retrasados y tiempo total
    Que le toma realizar esa solucion
    '''
    totalCost = 0
    for component in result:
        for product in result[component]:
           totalCost = totalCost + product.cost[component]+depCalc(component, product)
           print(product.days_left())
    return totalCost

def main():
    products = Product.import_csv('datos.csv')
    processes = []

    for product in products:
        for {process for process in range(1, 14)}

    best = {'vector': random_permutation(products)}


if __name__ == '__main__':
    main()

def random_permutation(products):
    pass
