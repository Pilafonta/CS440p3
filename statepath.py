'''
Written by Karl Shiffler (shiffler@bu.edu) 
	   and Peter LaFontaine (lafonta@bu.edu)

April 2, 2015
Usage is "python statepath.py file.hmm file.obs"

Takes two command line arguments, the first being the HMM definition file, 
and the second being the list of observations. It then calculates and prints 
the probability of the observed sequences. If the probability is nonzero, it 
also prints the most likely state path sequence. 

'''
import hmm
import csv
import numpy as np 
import sys

# define the HMM from the input file
# parse the observation sequences

hmmDef = []
obsDef = []

with open("./%s" %sys.argv[1], "rb") as infile:
	reader = csv.reader(infile, delimiter=" ")
	for row in reader:
		hmmDef.append(row)

with open("./%s" %sys.argv[2], "rb") as infile:
	reader = csv.reader(infile, delimiter=" ")
	for row in reader:
		obsDef.append(row)

numSent = int(obsDef[0][0])

a = np.array(hmmDef[4:8]).astype(float)
b = np.array(hmmDef[9:13]).astype(float)
pi = np.array(hmmDef[-1]).astype(float)

symList = np.array(hmmDef[2])

stateList = []
for stateNum in range(int(hmmDef[0][0])):
	stateList.append(hmm.state(hmmDef[1][stateNum], stateNum, pi[stateNum]))

connectList = []
for stateFrom in stateList:
	#print stateFrom.name, stateFrom.index, stateFrom.init
	for stateTo in stateList:
		if a[stateFrom.index][stateTo.index] > 0.0:
			connectList.append(hmm.connect(stateFrom, stateTo, a[stateFrom.index][stateTo.index]))

outputList = []
for origState in stateList:
	temp = []
	for i in range(int(hmmDef[0][1])):
		temp.append(hmm.output(origState, symList[i], b[origState.index][i], i))
	outputList.append(temp)

outputList = np.array(outputList)

del hmmDef[1][-1]


# compute base case for all starting observations
alpha1 = []
for x in range(len(outputList)):
	temp = []
	for l in outputList[x]:
		temp.append(l.b * l.origin.pi)
	alpha1.append(temp)
alpha1 = np.array(alpha1)

#compute and print the rest of the alphas
num = 1
for n in range(numSent): 	
	T = int(obsDef[num][0])
	obs = obsDef[num+1]
	num += 2

	objObs = []
	for o in obs:
		for row in outputList:
			for out in row:
				if out.outSym == o:
					objObs.append(out)

	ALPHA = np.zeros((T, len(hmmDef[1])))

	ind = objObs[0].index
	ALPHA[0] = alpha1[:,ind]

	for t in range(1,T):
		bjs=[]
		for j in range(len(ALPHA[t])):
			sumA = 0
			for i in range(len(ALPHA[t-1])):
				sumA += ALPHA[t-1][i] * a[i][j]
			bj = b[j][objObs[t*4].index]
			
			z = sumA * bj
			ALPHA[t,j] = z

	print sum(ALPHA[T-1])