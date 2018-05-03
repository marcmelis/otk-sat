import sys
import random

class Formula(object):
    def __init__(self, n_vars, max_flips=40):

        # [clause, clause,..]
        self.simple = []
        # [ [], [clause,clause,.], [clause,clause,..], ..]
        self.linked = [ [] for _ in xrange(n_vars * 2 + 1) ]
        self.n_vars = n_vars
        self.interpretation = range(n_vars + 1)
        self.max_flips = max_flips

    def add_clause(self, clause):
        self.simple.append(clause)
        for literal in clause:
            self.linked[literal].append(clause)

    def new_random_interpretation(self):
        for i in xrange(1, self.n_vars + 1):
            if random.random() < 0.5:
                self.interpretation[i] *= -1

    def is_satisfiable(self):
        pass

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
    while(1): # max_tries = infinite
        formula.new_random_interpretation()
        for _ in formula.max_flips:
            if formula.is_satisfiable():
                pass

def main():


    formula = Formula.parse(sys.argv[1])

    print formula.simple
    sys.exit(0)
    solution = run_sat(formula)

    solution += [x for x in range(1, formula.n_vars + 1) if x not in solution and -x not in solution]
    solution.sort(key=abs)
    print 's SATISFIABLE'
    print 'v ' + ' '.join([str(x) for x in solution]) + ' 0'


if __name__ == '__main__':
    main()