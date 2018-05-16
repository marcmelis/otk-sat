

def parse(filename):
    clauses = []
    count = 0
    lit_clause = [[]] #DEL
    n_vars = 0 #DEL
    for line in open(filename):

        if line[0] == 'c':
            continue
        if line[0] == 'p':
            n_vars = int(line.split()[2])
            index_clauses_lit = [ [] for _ in xrange(n_vars*2 +1)]
            continue

        clause = []
        for literal in line[:-2].split():
            literal = int(literal)
            clause.append(literal)
            lit_clause[literal].append(count)
        count += 1

    return clauses, n_vars, lit_clause


def main():
    #formula = Formula.parse("test.cnf")
    clauses, n_vars, lit_clause = parse(sys.argv[1])

    solution = run_sat(formula)

    print 's SATISFIABLE'
    print 'v ' + ' '.join(
        [str(literal + 1) if positive else str(-(literal + 1)) for literal, positive in
         enumerate(solution[1:])]) + ' 0'


if __name__ == '__main__':
    main()
