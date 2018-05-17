#!/usr/bin/env python
# coding=utf-8

"""
    SAT solver Local Search
    Course in Advanced Programming in Artificial Intelligence - UdL

"""

import random
import sys


class Formula(object):
    def __init__(self, n_vars):

        # [clause, clause,..]
        self.simple = []
        # [ [], [clause,clause,.], [clause,clause,..], ..]
        self.linked = [[] for _ in xrange(n_vars * 2 + 1)]
        self.n_vars = n_vars
        self.interpretation = [True for _ in xrange(n_vars + 1)]
        self.max_flips = n_vars * 3
        self.omega_prob = 0.2

    def add_clause(self, clause):
        self.simple.append(clause)
        for literal in clause:
            self.linked[literal].append(clause)

    def new_random_interpretation(self):
        for i in xrange(1, self.n_vars + 1):
            if random.random() < 0.5:
                self.interpretation[i] = not self.interpretation[i]

    def get_unsatisfied_clauses(self):
        unsatisfied_clauses = []
        for clause in self.simple:
            if not self.is_clause_satisfied(clause):
                unsatisfied_clauses.append(clause)
        return unsatisfied_clauses

    def is_clause_satisfied(self, clause):
        for literal in clause:
            if literal > 0:
                if self.interpretation[abs(literal)]:
                    return True
            else:
                if not self.interpretation[abs(literal)]:
                    return True
        return False

    @staticmethod
    def is_clause_satisfied_with_interpretation(clause, interpretation):
        for literal in clause:
            if literal > 0:
                if interpretation[abs(literal)]:
                    return True
            else:
                if not interpretation[abs(literal)]:
                    return True
        return False

    def unsatisfied_counter(self, literal):
        new_interpretation = self.interpretation[:]
        new_interpretation[literal] = not new_interpretation[literal]
        counter = 0
        for clause in self.linked[-literal]:
            if self.is_clause_satisfied(clause):
                if not Formula.is_clause_satisfied_with_interpretation(clause, new_interpretation):
                    counter += 1
        return counter

    def get_broken(self, clause):
        min_unsatisfied = sys.maxint
        for literal in clause:
            new_interpretation = self.interpretation[:]
            new_interpretation[abs(literal)] = literal

            unsatisfied_count = self.unsatisfied_counter(literal)
            if unsatisfied_count < min_unsatisfied:
                min_unsatisfied = unsatisfied_count
                best_literal = literal

        return best_literal, min_unsatisfied

    @staticmethod
    def parse(filename):
        for line in open(filename):
            if line[0] == 'c':
                continue
            if line[0] == 'p':
                formula = Formula(int(line.split()[2]))
                continue
            formula.add_clause([int(x) for x in line[:-2].split()])
        return formula


def run_sat(formula):
    count = 0
    while (1):  # max_tries = infinite

        formula.new_random_interpretation()
        count +=1
        print count
        for _ in xrange(formula.max_flips):

            unsatisfied_clauses = formula.get_unsatisfied_clauses()

            if not unsatisfied_clauses:
                return formula.interpretation

            unsatisfied_clause = random.choice(unsatisfied_clauses)

            best_literal, min_broken = formula.get_broken(unsatisfied_clause)

            if min_broken > 0 and random.random() <= formula.omega_prob:
                new_literal = random.choice(unsatisfied_clause)
            else:
                new_literal = best_literal

            formula.interpretation[abs(new_literal)] = not formula.interpretation[abs(new_literal)]


def main():
    formula = Formula.parse("test.cnf")
    #formula = Formula.parse(sys.argv[1])

    solution = run_sat(formula)

    print 's SATISFIABLE'
    print 'v ' + ' '.join(
        [str(literal + 1) if positive else str(-(literal + 1)) for literal, positive in
         enumerate(solution[1:])]) + ' 0'


if __name__ == '__main__':
    main()
