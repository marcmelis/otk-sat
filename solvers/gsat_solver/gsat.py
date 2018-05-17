#!/usr/bin/env python
# coding=utf-8

"""
    SAT solver Local Search
    Course in Advanced Programming in Artificial Intelligence - UdL

"""

import random
import sys
from itertools import repeat


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
        sl = clause
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
    max_flips = n_vars
    while True:
        assignment = initial_configuration(n_vars)
        max_sat = 0
        for flips in xrange(max_flips):
            if check_solution(assignment, formula):
                return assignment
            max_sat, x = max_sat_clauses(formula, assignment, max_sat)
            assignment[x] = -assignment[x]


def max_sat_clauses(formula, assignment, max_satisfied):
    max_sat = max_satisfied
    li = random.randint(0, len(assignment) - 1)  # Random Walk
    for i in range(0, len(assignment)):
        sat = 0
        choice = assignment[:]
        index = abs(choice[i]) - 1
        choice[index] = -choice[index]
        for clause in formula:
            if is_satisfied_clause(clause, choice):
                sat = sat + 1
                break
        if sat > max_sat:
            li = i
            max_sat = sat
            if max_sat == len(formula):
                break
    return max_sat, li


def is_satisfied_clause(clause, choice):
    for lit in clause:
        if lit in choice:
            return True
    return False


def initial_configuration(n_vars):
    init_conf = list()
    for i in range(1, n_vars + 1):
        prob = random.randint(0, 1)
        if prob == 1:
            init_conf.append(i)
        else:
            init_conf.append(-i)
    return init_conf


def lit_clause_struct(formula, n_vars):
    pos = [[] for i in repeat(None, n_vars + 1)]
    neg = [[] for i in repeat(None, n_vars + 1)]
    index_c = 1
    for clause in formula:
        index_l = 1
        for literal in clause:
            i = abs(literal)
            if literal > 0:
                pos[i].append(index_c)
            elif literal < 0:
                neg[i].append(index_c)
            index_l = index_l + 1
        index_c = index_c + 1
    return pos, neg


def main():
    formula, n_vars, n_clauses = parse(sys.argv[1])
    pos_list, neg_list = lit_clause_struct(formula, n_vars)
    print "Formula: ", formula
    print "Pos: ", pos_list
    print "Neg: ", neg_list
    solution = gsat(formula, n_vars)
    print 's SATISFIABLE'
    print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'


if __name__ == '__main__':
    main()
