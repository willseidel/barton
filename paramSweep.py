#This function accepts a list of possible parameters (paramVals) and the number of parameters per set (nSet).
#It returns a matrix with all possible sets combining those values of length nSet. 

import numpy as np

def paramSweep(paramVals,nSet):

	nGuessVal 	= len(paramVals)
	nComb 		= nGuessVal**nSet
	paramList 		= np.zeros((nComb,nSet))

	for i in range(0,nComb):
		for j in range(0,nSet):
				valIndex = (int(np.floor(i/(nGuessVal**(nSet - j - 1)))))%nGuessVal
				paramList[i][j] = paramVals[valIndex]

	return paramList


guess = [1e-5,1e-4,1e-3,1e-2,1e-1,1e0,1e1,1e2,1e3]
paramNumber = 3
params = paramSweep(guess,paramNumber)

print params