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

def gsat(formula, assignment):
    max_flips = 10
    max_tries = 10000
    for tries in range(1, max_tries):
        A = inital_configuration(formula)
        for flips in range(1, max_flips):
            if A satisfies formula:
                return A
            # Selecció de variable
            x = select-variable(A)
            A = A with x flipped
    return solution

def main():
    formula, n_vars = parse(sys.argv[1])

    solution = gsat(formula, [])
    print solution
    if check_solution(solution, formula):
        print 's SATISFIABLE'
        print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'
    else:
        print 's UNSATISFIABLE'


if __name__ == '__main__':
    main()
