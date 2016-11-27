
#this version loops through paramGridOrder and paramGridDensity making values of varying order at a given density. 
#These are then fed to paramsweep. We could call this 'multiOrderSweep' or something



for i in range(0,paramGridOrder):
	for k in range(0,paramGridDensity):
		paramGridValues += [((k+1)*(10/paramGridDensity))*(10**i)]
		paramGridValues += [-((k+1)*(10/paramGridDensity))*(10**i)]

paramSet = paramSweep(paramGridValues,len(params))

#this version loops through paramGridDensity and the number of params. It then creates a list of paramGridValues based on scalar 
#multiples of existing 'bestParams' (ie 0.9x 1.1x 0.8x 1.2x etc). This could be called 'singleOrderSweep'

		for k in range(1,paramGridDensity): #setting new tighter grid around 'best' values
			for l in range(0,len(params)):
				paramGridValues += [(1+(k/10.0))*bestParams[l]]
				paramGridValues += [-(1+(k/10.0))*bestParams[l]]

		paramSet = paramSweep(paramGridValues,len(params)) #new paramSet




###############OLD VERSION OF FUNCTION#############
#this function takes a set of parameter values and a number of parameters in each set.
#It then returns a list of sets that encompass all possible combinations of the values
#of length = nParams.
def paramSweep(paramVals,nParams):

	nComb 		= len(paramVals)**nParams #number of combinations
	paramList 	= np.zeros((nComb,nParams))

	for i in range(0,nComb):
		for j in range(0,nParams):
				valIndex = (int(np.floor(i/(len(paramVals)**(nParams - j - 1)))))%len(paramVals)
				paramList[i][j] = paramVals[valIndex]

	return paramList




