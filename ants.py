from datetime import datetime
from enum import Enum
from random import sample

import csv

dependencies = {1:set(),2:set(),3:set(),4:{1,2,3},5:{4},6:{4},7:{5,6},8:set(),9:{8},10:{9},11:set(),12:set(),13:{11,12},14:{13,10,7}}
FINAL_PHASE = 14


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
                              zip(range(1, FINAL_PHASE), row["Costo"].split(","))},
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
    best = {'vector': random_permutation(products)}
    return best['vector']


if __name__ == '__main__':
    main()


def get_all_initials(products):
    initials = set()

    for product in products:
        for initial in get_initials(product.passed_phases):
            initials.add(f'{product.id_}-{initial}')

    return initials


def random_permutation(products):
    current_initials = get_all_initials(products)
    solution = {phase: [] for phase in range(1, FINAL_PHASE)}

    final_initials = {f'{product.id_}-{FINAL_PHASE}' for product in products}

    while current_initials != final_initials:
        product_idx, phase = sample(current_initials, 1)[0].split('-')
        product_idx, phase = int(product_idx), int(phase)

        for product in products:
            if product.id_ == product_idx:
                product.passed_phases.add(phase)
                if phase != FINAL_PHASE:
                    solution[phase].append(product)
                break

        current_initials = get_all_initials(products)

    return solution


def get_initials(passed_phases, current_initials={FINAL_PHASE}):
    new_initials = set()
    final_initials = set()
    for process in current_initials:
        if not dependencies[process] - passed_phases:
            return {process}
        for dependency in dependencies[process] - passed_phases:
            new_initials = {dependency}
            dep = get_initials(passed_phases, new_initials)
            final_initials = final_initials.union(dep)
        return final_initials
