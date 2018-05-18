import random
import sys


def parse(filename):
    clauses = []
    count = 0
    for line in open(filename):
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            lit_clause = [[] for _ in xrange(n_vars * 2 + 1)]
            continue
        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        clauses.append(clause)
        count += 1
    return clauses, n_vars, lit_clause


def get_random_interpretation(n_vars):
    return [i if random.random() < 0.5 else -i for i in xrange(n_vars + 1)]


def get_true_sat_lit(clauses, interpretation):
    true_sat_lit = [0 for _ in clauses]
    for index, clause in enumerate(clauses):
        for lit in clause:
            if interpretation[abs(lit)] == lit:
                true_sat_lit[index] += 1
    return true_sat_lit


def update_tsl(literal_to_flip, true_sat_lit, lit_clause):
    for clause_index in lit_clause[literal_to_flip]:
        true_sat_lit[clause_index] += 1
    for clause_index in lit_clause[-literal_to_flip]:
        true_sat_lit[clause_index] -= 1


def compute_broken(clause, true_sat_lit, lit_in_clauses, interpretation, omega=0.4):
    break_min = sys.maxint
    best_literals = []
    for literal in clause:

        break_score = 0

        if interpretation[abs(literal)] < 0:
            for clause_index in lit_in_clauses[-abs(literal)]:
                if true_sat_lit[clause_index] == 1:
                    break_score += 1
        else:
            for clause_index in lit_in_clauses[abs(literal)]:
                if true_sat_lit[clause_index] == 1:
                    break_score += 1

        if break_score < break_min:
            break_min = break_score
            best_literals = [literal]
        elif break_score == break_min:
            best_literals.append(literal)

    if break_min != 0 and random.random() < omega:
        best_literals = clause

    return random.choice(best_literals)


def most_often_broken_clauses_heuristic(lit_clause, unsatisfied_clause):
        aux = []
        lit = 0
        max_len = 1
        print "\n"
        print "Unsat clause: ", unsatisfied_clause
        for literal in unsatisfied_clause:
            length = len(lit_clause[literal])
            if length >= max_len:
                max_len = length
                lit = literal
            aux.append(lit_clause[literal])
        print "max_len: ", max_len, " -  literal: ", lit
        print "aux: ", aux
        print "\n"
        return lit


def run_sat(clauses, n_vars, lit_clause, max_flips_proportion=3):
    max_flips = n_vars * max_flips_proportion
    print "Len: ", n_vars
    print "Len:1 ", len(lit_clause)
    print "Lit clause: ", lit_clause
    print "Max len sublist: ", max(lit_clause, key=len)
    while 1:
        interpretation = get_random_interpretation(n_vars)
        true_sat_lit = get_true_sat_lit(clauses, interpretation)

        for _ in xrange(max_flips):
            unsatisfied_clauses_index = [index for index, true_lit in enumerate(true_sat_lit) if not true_lit]

            if not unsatisfied_clauses_index:
                return interpretation

            clause_index = random.choice(unsatisfied_clauses_index)

            unsatisfied_clause = clauses[clause_index]

            # lit_to_flip = most_often_broken_clauses_heuristic(lit_clause, unsatisfied_clause)
            lit_to_flip = compute_broken(unsatisfied_clause, true_sat_lit, lit_clause, interpretation)

            update_tsl(lit_to_flip, true_sat_lit, lit_clause)

            interpretation[abs(lit_to_flip)] *= -1


def main():
    clauses, n_vars, lit_clause = parse(sys.argv[1])
    solution = run_sat(clauses, n_vars, lit_clause)
    print 's SATISFIABLE'
    print 'v ' + ' '.join(map(str, solution[1:])) + ' 0'


if __name__ == '__main__':
    main()
