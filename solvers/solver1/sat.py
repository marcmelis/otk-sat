#!/usr/bin/env python
# coding=utf-8

"""
    SAT solver Local Search
    Course in Advanced Programming in Artificial Intelligence - UdL

"""

import sys
import random
from copy import deepcopy


def parse(filename):
    clauses = []
    for line in open(filename):
        if line.startswith('c'):
            continue
        if line.startswith('p'):
            n_vars, n_clauses = line.split()[2:4]
            continue
        clause = [int(x) for x in line[:-2].split()]
        clauses.append(clause)
    return clauses, int(n_vars), int(n_clauses)


def random_variable_selection(n_vars):
    return random.randint(0, n_vars - 1)


def max_sat_clauses(formula, assignment, max_satisfied):
    max_sat = max_satisfied
    li = random.randint(0, len(assignment) - 1)  # Random Walk
    for i in range(0, len(assignment)):
        sat = 0
        choice = deepcopy(assignment)
        index = abs(choice[i]) - 1
        choice[index] = -choice[index]
        for clause in formula:
            for lit in clause:
                if lit in choice:
                    sat = sat + 1
                    break
        if sat > max_satisfied:
            li = i
            max_sat = sat
    return max_sat, li


def get_counter(formula):
    counter = {}
    for clause in formula:
        for literal in clause:
            if literal in counter:
                counter[literal] += 1
            else:
                counter[literal] = 0
    return counter


def check_solution(solution, formula):
    for clause in formula:
        solution = map(int, solution)
        sl = map(int, clause)
        length = len(sl)
        for lit in sl:
            if lit == solution[abs(lit) - 1]:
                break
            else:
                length -= 1
        if length == 0:
            return False
    return True


def gsat(formula, n_vars):
    max_flips = n_vars * n_vars
    max_tries = 10
    while True:
        assignment = initial_configuration(n_vars)
        max_sat = 0
        for tries in range(1, max_tries):
            for flips in range(1, max_flips):
                if check_solution(assignment, formula):
                    return assignment
                max_sat, x = max_sat_clauses(formula, assignment, max_sat)
                assignment[x] = -assignment[x]


def initial_configuration(n_vars):
    init_conf = list()
    for i in range(1, n_vars + 1):
        prob = random.randint(0, 1)
        if prob == 1:
            init_conf.append(i)
        else:
            init_conf.append(-i)
    return init_conf


def main():
    formula, n_vars, n_clauses = parse(sys.argv[1])
    solution = gsat(formula, n_vars)
    print 's SATISFIABLE'
    print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'


if __name__ == '__main__':
    main()
