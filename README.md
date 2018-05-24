# LocalSearchSat

You can find a copy of this repository at https://github.com/markankaro/walksat_practice.

All the formulas are in [DIMACS format].

[DIMACS format]: http://www.satcompetition.org/2004/format-solvers2004.html

## Solver

Simple Python implementation of a WalkSAT Solver using the data structures proposed by Shaowei Cai. 

```
$ python src/otk_sat.py <formula_to_solve>
```

## Formula generator

CNF formula generator.

```
$ python src/rnd_cnf_gen.py <num_vars> <num_clauses> <clauses_length> [<seed>] [ > file ]
```

## Graph Coloring

Graph coloring problem generator. 

```
$ python src/rnd_graph_gen.py <num-nodes> <edge-prob> <num-colors> <solver-name> [<random-seed>]
```

Output image saved as `out.png`. Original CNF saved as `input.cnf` and satisfiabilty of this CNF saved as `output.cnf`.

### Requirements

- networkx library


### Example of usage

```
$ python src/rnd_graph_gen.py 10 0.3 5 src/otk_sat.py [<random-seed>]
```
\**The script will not finish if the formula of the graph generated is unsatisfiable if you use a local search solver*

## Solution validator

Validator for SATISFIABLE formulas.

```
$ python src/sat_val.py <formula> <solution>
```

## References: 
* Shaowei Cai, Faster Implementation for WalkSAT (2013). http://lcs.ios.ac.cn/~caisw/Paper/Faster_WalkSAT.pdf

