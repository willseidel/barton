#This function accepts a list of possible parameters (paramVals) and the number of parameters per set (nSet).
#It returns a matrix with all possible sets combining those values of length nSet. 

import numpy as np

def paramSweep(paramVals,nSet):

	nGuessVal 	= len(paramVals)
	nComb 		= nGuessVal**nSet
	params 		= np.zeros((nComb,nSet))

	for i in range(0,nComb):
		for j in range(0,nSet):
				valIndex = (int(np.floor(i/(nGuessVal**(nSet - j - 1)))))%nGuessVal
				params[i][j] = paramVals[valIndex]

	return params


guess = [1,2,3,4]
paramNumber = 3
params = paramSweep(guess,paramNumber)

print params