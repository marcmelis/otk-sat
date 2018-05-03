#!/usr/bin/env python
# coding=utf-8

"""
    SAT solver Local Search
    Course in Advanced Programming in Artificial Intelligence - UdL

"""

import sys
import random


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
    return clauses, int(n_vars)


def random_variable_selection(n_vars):
    return random.randint(0, n_vars - 1)


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
    max_flips = 100000
    max_tries = 100
    while True:
        assignment = initial_configuration(n_vars)
        for tries in range(1, max_tries):
            for flips in range(1, max_flips):
                if check_solution(assignment, formula):
                    return assignment
                x = random_variable_selection(n_vars)
                # print "Variable selected: ", x + 1, " - Solution: ", assignment
                assignment[x] = -assignment[x]
                # print "Solution Flipped: ", assignment


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
    formula, n_vars = parse(sys.argv[1])
    solution = gsat(formula, n_vars)
    if check_solution(solution, formula):
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    main()
