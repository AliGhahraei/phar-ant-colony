from datetime import datetime
from enum import Enum

dependencies = {1:{1:[],2:[],3:[],4:[1,2,3],5:[4],6:[4],7:[5,6]},2:{1:[],2:[1],3:[3]},3:{1:[],2:[],3:[1,2]}}

class Product():
    def __init__(self, cost, name, date):
        self.cost = cost
        self.name = name
        self.date = date

    def days_left(self):
        return datetime.now() - self.date

#Calcula el costo de un resultado de combinancion usando el numero de pedidos retrasados y tiempo total
#Que le toma realizar esa solucion.
def cost(result):
    for component in result:
        for product in result[component]:
            if product.


