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
		self.pi = float(pi) #* 1000

class connect:
	'''
	Connections between states. Parameters include originating state, the 'to' state and the 
	probability of following that connection (a)
	'''
	def __init__(self, orig, to, a):
		self.origin = orig
		self.to = to
		self.a = float(a) #* 1000

class output:
	'''
	Defines output probabilities. Parameters include the originating state, the symbol to be output,
	and the probability of that symbol being output (b)
	'''
	def __init__(self, orig, outSym, b):
		self.origin = orig
		self.outSym = outSym
		self.b = float(b) #* 1000
