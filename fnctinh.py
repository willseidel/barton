#this is scratch work to figure out inheritence in python
import numpy as np


###############NEW VERSION OF FUNCTION#############
class paramSet(object):
	#this class deals with the creation and manipulation of sets of parameters.

	def __init__(self, gridOrder,gridDensity, nParamsPerSet):    
		self.gridOrder 		= gridOrder 	#number of orders of magnitude in initial grid
		self.gridDensity 	= gridDensity 	#number of grid points per order of magnitude
		self.nParamsPerSet 	= nParamsPerSet #number of parameters per set 

	def paramSweep(self, paramVals, nParamsPerSet):
		#this function takes a set of parameter values. It then returns a list of sets that
		#encompass all possible combinations of the values of length = nParamsPerSet.
		nComb 			= len(paramVals)**self.nParamsPerSet #number of combinations
		self.paramList 	= np.zeros((nComb,self.nParamsPerSet))
		self.paranList = []
		for i in range(0,nComb):
			for j in range(0,self.nParamsPerSet):
					valIndex = (int(np.floor(i/(len(paramVals)**(self.nParamsPerSet - j - 1)))))%len(paramVals)
					self.paramList[i][j] = paramVals[valIndex]
		return self.paramList 	#list of parameter sets

	def multiOrderSweep(self):
	#this function loops through gridOrder and gridDensity making values of varying
	#order at a given density. These are then fed to paramsweep to make all combinations.

		paramGridValues 	= []
		for i in range(0,self.gridOrder):
			for k in range(0,self.gridDensity):
				paramGridValues += [((k+1)*(10/self.gridDensity))*(10**i)]
				paramGridValues += [-((k+1)*(10/self.gridDensity))*(10**i)]

		return self.paramSweep(paramGridValues,self.nParamsPerSet)

	def singleOrderSweep(self,bestParams):
	#this function loops through gridDensity and the number of params.
	#It then creates a list of paramGridValues based on scalar 
	#multiples of existing 'bestParams' (ie 0.9x 1.1x 0.8x 1.2x etc). 
	#These are then fed to paramsweep to make all combinations.

		paramGridValues 	= []
		for k in range(1,self.gridDensity): #setting new tighter grid around 'best' values
			for l in range(0,self.nParamsPerSet):
				paramGridValues += [(1+(k/10.0))*bestParams[l]]
				paramGridValues += [-(1+(k/10.0))*bestParams[l]]

		self.paramSweep(paramGridValues,self.nParamsPerSet) #new paramSet
	



whsParams = paramSet(2,2,3)
bestParams = [1,2,3]
#whsParams.paramSweep(params,2)

whsParams.multiOrderSweep()
print whsParams.paramList
print len(whsParams.paramList)
whsParams.singleOrderSweep(bestParams)
print whsParams.paramList
print len(whsParams.paramList)