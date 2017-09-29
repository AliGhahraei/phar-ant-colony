from datetime import datetime
from enum import Enum
from random import sample
from datetime import timedelta
import numpy as np

import csv

dependencies = {1:set(),2:set(),3:set(),4:{1,2,3},5:{4},6:{4},7:{5,6},8:set(),9:{8},10:{9},11:set(),12:set(),13:{11,12},14:{13,10,7}}
FINAL_PHASE = 14
solution_path = []


class Product():
    def __init__(self, cost, name, date, id_, passed_phases=None, original_phases=None):
        self.cost = cost
        self.name = name
        self.date = date
        self.passed_phases = passed_phases or set()
        self.original_phases = original_phases or set()
        self.id_ = id_

    def hours_left(self):
        if self.date > datetime.now():
            hours = abs(self.date - datetime.now())
        else:
            hours = timedelta(minutes=0)
        return hours.total_seconds() / 3600

    def import_csv(path):
        products = []
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for idx, row in enumerate(reader):
                try:
                    products.append(
                        Product(
                            id_=idx,
                            cost={key: int(value) for (key, value) in
                                  zip(range(1, FINAL_PHASE), row["Costo"].split(","))},
                            name=row['Producto'],
                            date=datetime.strptime(row['Fecha'], '%d/%m/%Y %H:%M'),
                            passed_phases={int(x) for x in
                                           row["Fases Pasadas"].split(",")},
                            original_phases={int(x) for x in
                                           row["Fases Pasadas"].split(",")}))
                except: 
                    products.append(
                        Product(
                            id_=idx,
                            cost={key: int(value) for (key, value) in
                                  zip(range(1, FINAL_PHASE), row["Costo"].split(","))},
                            name=row['Producto'],
                            date=datetime.strptime(row['Fecha'], '%d/%m/%Y %H:%M'),
                            passed_phases=set(),
                            original_phases=set()))

                products[-1].cost[14] = 0
        return products


def depCalc(root,prod):
    '''Calcula dependencia'''
    costAcum = 0
    if root in prod.original_phases:
        return 0
    if len(dependencies[root]) != 0:
        #dependency_cost = [prod.cost[dependency] for dependency in dependencies[root]]
        costAcum += prod.cost[root] + depCalc(max(dependency_cost), prod)
        return costAcum
    else:
        return prod.cost[root]

def cost(result, products):
    phase_start_times = {phase: 0 for phase in range(1, FINAL_PHASE)}

    for phase_idx in range(1, FINAL_PHASE):
        max_dep_value = 0

        try:
            first_product = result[phase_idx][0]

            for dependency in dependencies[phase_idx] - first_product.original_phases:
                phase_time = 0

                for product in result[dependency]:
                    phase_time += product.cost[dependency]
                    if product is first_product:
                        if phase_start_times[dependency] + phase_time >= max_dep_value:
                            max_dep_value = phase_start_times[dependency] + phase_time
                        break

        except IndexError:
            pass

        phase_start_times[phase_idx] = max_dep_value


    total_delay = 0

    for product in products:
        max_dependency_duration = 0

        for dependency in dependencies[FINAL_PHASE] - product.original_phases:
            phase_time = 0

            phase_time += calculate_dependency_cost(product, dependency, result)
            if (phase_start_times[dependency] + phase_time >= max_dependency_duration):
                max_dependency_duration = phase_start_times[dependency] + phase_time



        expected_delivery = datetime.now() + timedelta(hours=max_dependency_duration)
        product_delay = expected_delivery - product.date

        if product_delay > timedelta(hours=0):
            total_delay += product_delay.total_seconds()

    return total_delay

    #return max([phase_start_times[dep] for dep in dependencies[FINAL_PHASE]])


    #return component_duration

def calculate_dependency_cost(product, dependency, result):
    max_dependency_duration = 0
    phase_time = 0
    if dependencies[dependency] - product.original_phases != set():
        for phase_product in result[dependency]:
            phase_time += phase_product.cost[dependency]
            if phase_product is product:
                phase_time += phase_product.cost[dependency]
    else:
        return 0

    temporal_phase_time = 0
    for dep in dependencies[dependency] - product.original_phases:
        t2 = calculate_dependency_cost(product, dep, result)
        if t2 > temporal_phase_time:
            temporal_phase_time = t2
        else:
            return phase_time

    return phase_time + temporal_phase_time

def initialise_pheromone_matrix(num_products, naive_score):
    """initialises the pheromone matrix"""
    if naive_score == 0:
        naive_score = .000000000000000001
    v = (num_products*(FINAL_PHASE-1)) / naive_score
    return v * np.ones((num_products*(FINAL_PHASE-1))*(num_products*(FINAL_PHASE-1))).reshape((num_products*(FINAL_PHASE-1),(num_products*(FINAL_PHASE-1))))

def calculate_choices(processes, products, current_node, pheromone, c_heur, c_hist):
    """calculate the selection probability for a group of processes"""
    choices = []
    for i,coord in enumerate(processes):
        product_idx, phase = coord.split('-')
        product_idx, phase = int(product_idx), int(phase)
        prob = {'process' : (product_idx, phase)}
        costs = {product.id_: product.cost for product in products}
        if phase != 14:
            prob['history'] = pheromone[current_node[0]*13 + current_node[1] - 1, product_idx*13 + phase - 1] ** c_hist
            prob['distance'] = costs[product_idx][phase]
        else:
            prob['distance'] = 1
            prob['history'] = 0
        prob['heuristic'] = (1.0 / prob['distance']) ** c_heur
        prob['prob'] = prob['history'] * prob['heuristic']
        choices.append(prob)
    return choices


def select_next_process(choices):
    """selects the next process for a partial tour"""
    psum = 0.0
    for element in choices: psum += element['prob']
    if psum == 0.0:
        return choices[np.random.randint(len(choices))]['process']
    v = np.random.random()
    for i,choice in enumerate(choices):
        v -= choice['prob'] / psum
        if v <= 0.0: return choice['process']
    return choices[-1]['process']


def stepwise_const(products, phero, c_heur, c_hist):
    """construct a tour for an ant"""
    current_initials = get_all_initials(products)

    solution = {phase: [] for phase in range(1, FINAL_PHASE)}
    final_initials = {f'{product.id_}-{FINAL_PHASE}' for product in products}
    product_idx, phase = sample(current_initials, 1)[0].split('-')
    product_idx, phase = int(product_idx), int(phase)
    perm = {phase: [] for phase in range(1, FINAL_PHASE)}
    while current_initials != final_initials:
        possible_processes = get_all_initials(products)
        choices = calculate_choices(possible_processes, products, (product_idx, phase), phero, c_heur, c_hist)
        next_process = select_next_process(choices)
        for product in products:
            if product.id_ == next_process[0]:
                perm[next_process[1]].append(product)
                solution_path.append((product.id_, next_process[1], product.cost[next_process[1]]))
                product.passed_phases.add(next_process[1])
        current_initials = get_all_initials(products)
    return perm


def decay_pheromone(pheromone, decay_factor):
    """reduce all the pheromone values"""
    factor = 1.0 - decay_factor
    for i in range(len(pheromone)):
        for j in range(len(pheromone[0])):
            pheromone[i, j] *= factor
    
def update_pheromone(pheromone, solutions):
    """increase the pheromone values in the ants tours"""
    for other in solutions:
        current_idx, current_phase, current_cost = other[0]

        for idx, phase, cost in other[1:]:
            pheromone[idx*13 + phase - 1,current_idx*13 + current_phase - 1] += 1.0 / cost
            pheromone[current_idx*13 + current_phase - 1,idx*13 + phase - 1] += 1.0 / cost

            current_idx, current_phase, current_cost = idx, phase, cost


def get_all_initials(products):
    initials = set()

    for product in products:
        for initial in get_initials(product.passed_phases):
            initials.add(f'{product.id_}-{initial}')

    return initials


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


def main():
    global solution_path
    num_ants = 3
    max_it = 20
    c_heur = 2.5 # heuristic coefficient
    c_hist = 1.0 # pheromone coefficient
    decay_factor = 0.6 # reduction of pheromone
    processes = []
    products = Product.import_csv("datos.csv")
    best = {'vector': random_permutation(products)}
    best['cost'] = cost(best['vector'], products)
    pheromone = initialise_pheromone_matrix(len(products), best['cost'])
    for i in range(max_it):
        solutions = []
        for ant in range(num_ants):
            candidate = {}
            products = Product.import_csv("datos.csv")
            candidate['vector'] = stepwise_const(products, pheromone, c_heur, c_hist)
            candidate['cost'] = cost(candidate['vector'], products)
            if candidate['cost'] < best['cost']:
                best = candidate
            solutions.append(solution_path)
            solution_path = []
        decay_pheromone(pheromone, decay_factor)
        update_pheromone(pheromone, solutions)
        print(" > iteration=%d, best=%g" % (i+1,best['cost']))

    nuBest = {phase: [] for phase in range(1, FINAL_PHASE)}
    for i in best["vector"]:
        for j in best["vector"][i]:
            nuBest[i].append(j.name)


    print(nuBest)
    return best


if __name__ == '__main__':
    main()
