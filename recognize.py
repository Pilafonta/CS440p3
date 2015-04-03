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

numSent = int(obsDef[0][0])

a = np.array(hmmDef[4:8]).astype(float)
b = np.array(hmmDef[9:13]).astype(float)
pi = np.array(hmmDef[-1]).astype(float)

a *= 1000
b *= 1000
pi*= 1000

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
		temp.append(hmm.output(origState, symList[i], b[origState.index][i], i))
	outputList.append(temp)

outputList = np.array(outputList)

del hmmDef[1][-1]






def forHelp(alpha):
	#recursive call
	alphaNext = []
	for x in outputList:
		alphaNext.append(alpha*sum(x.b*x.origin.a))
	forHelp(alphaNext)



# compute base case for all starting observations
alpha1 = []
for x in range(len(outputList)):
	temp = []
	for l in outputList[x]:
		temp.append(l.b * l.origin.pi)
	alpha1.append(temp)
alpha1 = np.array(alpha1)
# forHelp(np.array(alpha1)[:,0])

num = 1
# for loop here for number of sentences ot be recognized DONT FORGET
T = int(obsDef[num][0])
obs = obsDef[num+1]
num += 2

objObs = []
for o in obs:
	for row in outputList:
		for out in row:
			if out.outSym == o:
				# print out.origin.name
				objObs.append(out)

for x in objObs:
	print x.outSym, x.b, x.index#, x.origin.index

ALPHA = np.zeros((T, len(hmmDef[1])))

ind = objObs[0].index
ALPHA[0] = alpha1[:,ind]

# print "ALPHA = "
# print ALPHA
# print "a = "
# print a
print b

for t in range(1,T):
	bjs=[]
	for j in range(len(ALPHA[t])):
		sumA = 0
		for i in range(len(ALPHA[t-1])):
			sumA += ALPHA[t-1][i] * a[i][j]
		bj = b[j][objObs[t*4].index]
		# print sumA, bj, sumA * bj
		bjs.append(bj)
		print i, j
		print sumA, "---", bj
		print "mult", sumA * bj
		ALPHA[t,j] =  sumA #* bj
	# for j in range(len(ALPHA[t])): 
	# 	ALPHA[t][j] *= bjs[j]  

print ALPHA