#!/usr/bin/env python

import sys

def parse( filename ) :
	clauses = []
	for line in open( filename ) :
		if line.startswith( 'c' ) : continue
		if line.startswith( 'p' ) : continue
		clause = [ int(x) for x in line[:-2].split() ]
		clauses.append( clause )
	return clauses

def bcp( formula, unit ) :
	modified = []
	for clause in formula :
		if unit in clause : continue
		if -unit in clause :
			c = [ x for x in clause if x != -unit ]
			if len( c ) == 0 : return -1
			modified.append( c )
		else :
			modified.append( clause )
	return modified

def get_counter( formula ) :
	counter = {}
	for clause in formula :
		for literal in clause :
			if literal in counter :
				counter[ literal ] += 1
			else :
				counter[ literal ] = 0
	return counter

def pure_literal( formula, counter, assignment ) :
	pures = [] # [ x for x,y in counter.items() if -x not in counter ]
	for literal, times in counter.items() :
		if -literal not in counter : pures.append( literal )
	for pure in pures :
		formula = bcp( formula, pure )
	assignment += pures
	return formula

def backtracking( formula, assignment ) :
	counter = get_counter( formula )
	formula = pure_literal( formula, counter, assignment )
	if not formula :
		return assignment
	unit_clauses = [ c for c in formula if len( c ) == 1 ]
	while len( unit_clauses ) > 0 :
		unit = unit_clauses[ 0 ]
		formula = bcp( formula, unit[0] )
		assignment += [ unit[0] ]
		if formula == -1 :
			return []
		if not formula :
			return assignment
		unit_clauses = [ c for c in formula if len( c ) == 1 ]
	variable = max( counter )
	solution = backtracking( bcp( formula, variable ), assignment + [variable] )
	if not solution :
		solution = backtracking( bcp( formula, -variable ), assignment + [-variable] )
	return solution

def main() :
	clauses = parse( sys.argv[1] )
	solution = backtracking( clauses, [] )
	print ' '.join( [ str(x) for x in solution ] )

if __name__ == '__main__':
	main()
