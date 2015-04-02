import hmm
import csv
import numpy as np 
import sys

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

numObs = int(obsDef[0][0])

a = np.array(hmmDef[4:8])
b = np.array(hmmDef[9:13])
pi = np.array(hmmDef[-1])

symList = np.array(hmmDef[2])

#print a, "\n", b, "\n", pi

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
		temp.append(hmm.output(origState, symList[i], b[origState.index][i]))
	outputList.append(temp)
outputList = np.array(outputList)


def forHelp(alpha):
	#recursive call
	alphaNext = []
	for x in outputList:
		alphaNext.append(alpha*sum(x.b*x.origin.a))
	forHelp(alphaNext)

def forward():
	alpha1 = []
	# base case
	for x in range(len(outputList)):
		temp = []
		for l in outputList[x]:
			temp.append(l.b * l.origin.pi)
		alpha1.append(temp)
	#print np.array(alpha1)[:,0]
	forHelp(np.array(alpha1)[:,0])

	print np.array(alpha1)

print obsDef

num = 1
for i in range(numObs):
	T = obsDef[num]
	num += 2
	


# forward()

