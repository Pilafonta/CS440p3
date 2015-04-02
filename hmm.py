import csv
import numpy as np 
import sys

class state:
	'''
	Class defines states, including the name (Subject, Auxiliary, Predicate or Object), the index
	for use with determining probabilities and initialization probability (pi)
	'''
	def __init__(self, name, ix, pi):
		self.name = name
		self.index = ix
		self.init = pi

class connect:
	'''
	Connections between states. Parameters include originating state, the 'to' state and the 
	probability of following that connection (a)
	'''
	def __init__(self, orig, to, a):
		self.origin = orig
		self.to = to
		self.prob = a

class output:
	'''
	Defines output probabilities. Parameters include the originating state, the symbol to be output,
	and the probability of that symbol being output (b)
	'''
	def __init__(self, orig, outSym, b):
		self.origin = orig
		self.outSym = outSym
		self.prob = b

def main():
	hmmDef = []
	obsDef = []

	# print sys.argv

	with open("./%s" %sys.argv[1], "rb") as infile:
		reader = csv.reader(infile, delimiter=" ")
		for row in reader:
			hmmDef.append(row)

	with open("./%s" %sys.argv[2], "rb") as infile:
		reader = csv.reader(infile, delimiter=" ")
		for row in reader:
			obsDef.append(row)

	a = np.array(hmmDef[4:8])

	b = np.array(hmmDef[9:13])

	pi = np.array(hmmDef[-1])

	symList = np.array(hmmDef[2])

	# print a, "\n", b, "\n", pi

	stateList = []
	for stateNum in range(int(hmmDef[0][0])):
		stateList.append(state(hmmDef[1][stateNum], stateNum, pi[stateNum]))

	connectList = []
	for stateFrom in stateList:
		# print stateFrom.name, stateFrom.index
		for stateTo in stateList:
			if a[stateFrom.index][stateTo.index] > 0.0:
				connectList.append(connect(stateFrom, stateTo, a[stateFrom.index][stateTo.index]))

	outputList = []
	for origState in stateList:
		for i in range(int(hmmDef[0][1])):
			outputList.append(output(origState, symList[i], b[origState.index][i]))

	# for o in outputList:
	# 	print o.origin.name, o.outSym, o.prob

	# for c in connectList:
	# 	print c.origin.name, c.to.name, c.prob

if __name__ == "__main__": main()