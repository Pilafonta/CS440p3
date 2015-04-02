import csv
import numpy as np 

hmmDef = []
obsDef = []

with open("./sentence.hmm", "rb") as infile:
	reader = csv.reader(infile, delimiter=" ")
	for row in reader:
		hmmDef.append(row)

with open("./example1.obs", "rb") as infile:
	reader = csv.reader(infile, delimiter=" ")
	for row in reader:
		obsDef.append(row)

# print hmmDef
# print obsDef

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

a = np.array(hmmDef[4:8])

b = np.array(hmmDef[9:13])

print a, "\n", b

# stateList = []
# for stateNum in range(hmmDef[0][0]):
# 	stateList.append(state(hmmDef[1][stateNum], stateNum, hmmDef[-1][stateNum]))