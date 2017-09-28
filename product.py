from datetime import datetime
from enum import Enum

dependencies = {1:set(),2:set(),3:set(),4:{1,2,3},5:{4},6:{4},7:{5,6},8:[],9:[8],10:[9],11:[],12:[],13:[11,12],14[13,10,7]}


class Product():
    def __init__(self, cost, name, date):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = set()

    def days_left(self):
        return datetime.now() - self.date

#Calcula dependencia
def depCalc(root,prod):
    costAcum = 0
    if root in dependencies:
        for i in dependencies[root]:
            costAcum = costAcum + depCalc(i,prod)
        return costAcum
    else:
        return prod.cost[root]

#Calcula el costo de un resultado de combinancion usando el numero de pedidos retrasados y tiempo total
#Que le toma realizar esa solucion
def cost(result):
    totalCost = 0
    for component in result:
        for product in result[component]:
            totalCost + depCalc(component, product)
    return totalCost


def main():
    #result = {13:Product({1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:11,12:12,13:13},"tractor",datetime.today()),10:Product(),7:Product()}
    print("diego")
    #products = None
    #best = {'vector': random_permutation(products)}


if __name__ == '__main__':
    main()

def random_permutation(products):
    pass
