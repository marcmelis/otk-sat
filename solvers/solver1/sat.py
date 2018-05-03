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


def random_variable_selection(formula):
    counter = get_counter(formula)
    return random.choice(counter.keys())


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
            print solution
            print lit, solution[abs(lit) - 1]
            if lit == solution[abs(lit) - 1]:
                break
            else:
                length -= 1
        if length == 0:
            return False
    return True


"""def gsat(formula, assignment, n_vars):
    max_flips = 10
    max_tries = 1
    for tries in range(1, max_tries):
        A = initial_configuration(n_vars)
        for flips in range(1, max_flips):
            if A satisfies formula:
                return A
            # Selecció de variable
            x = select-variable(A)
            A = A with x flipped
    return solution"""


def initial_configuration(n_vars):
    init_conf = list()
    for i in range(1, n_vars + 1):
        init_conf.append(i)
    return init_conf


def main():
    formula, n_vars = parse(sys.argv[1])
    A = initial_configuration(n_vars)
    print A
    """solution = gsat(formula, [], n_vars)
    print solution
    if check_solution(solution, formula):
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'
"""


if __name__ == '__main__':
    main()
