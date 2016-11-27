import numpy as np
import gym

def evalParamSet(env,nRuns,divs,nAcs,params,render):
	#this function runs nRuns simulations using a set of parameters to evaluate
	#the highest reward that the parameter set produces

	rewardRecord = []

	for j in range(nRuns): #looping through simulations

		justImproved = False

		observation = env.reset()
		reward_cum = 0

		for i in range(nSteps): #looping through time in each simulation

			####INSERT LOGIC TO DECIDE ACTION
			action = 999
			obsDot = np.dot(params,observation)
			for k in range(0,nAcs-1):
				#print "k:",k
				if obsDot>divs[k]:
					action = actionOptions[k]
					break
				else:
					action = actionOptions[k+1]
			
			#######^^^^^^##############

			observation, reward, done, info  = env.step(action)
			if (render and j==0):
				env.render()
			if done:
				break

			reward_cum += reward


		rewardRecord += [reward_cum]

	return np.mean(rewardRecord)

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

		self.paramSweep(paramGridValues,self.nParamsPerSet)

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


#the environment
environmentName = 'MountainCar-v0'
env 			= gym.make(environmentName)

#inputs
nSteps 				= 500
nRunsAvg 			= 1
nRunsMax			= 10
paramGridOrder		= 5 	#search grid will go up/down by this many orders of magnitude
paramGridDensity 	= 1 	#number of elements in grid per order (ie order 1e0 w/density=5)...
							#includes 2 4 6 8 10

#initializing other variables
actionOptions 		= []
dotSpaceMax			= 1 #this is the magnitude that will govern the binning of actions based...
divs				= []	
rewardMeanRecord 	= []
paramGridValues 	= []
bestReward 			= -10e10
nRunsCum 			= 0 #total number of runs
nParams 			= 0 #number of parameters to optimize 


#this section just finds the range of discrete actions
for i in range(100):
	actionSample = env.action_space.sample() #getting sample
	if actionSample not in actionOptions:
		actionOptions += [actionSample]

nAcs = len(actionOptions) #number of actions
nObs = len(env.observation_space.sample()) #number of observation indices

#parameters we optimize
for i in range(0,nObs):
	nParams += 1

#finding where to set bin divisions for assigning actions
if nAcs ==2: #special case
	divs = [0]
else: #
	for i in range(1,nAcs):
		divs += [dotSpaceMax - (i-1)*((2*dotSpaceMax)/(nAcs-2))]

myParams 	= paramSet(paramGridOrder,paramGridDensity,nParams) #initializing parameter instance
myParams.multiOrderSweep() #creating coarse multi-order sweep to produce set of parameter sets

bestParams = myParams.paramList[1] #arbitratily setting 'best' parameter set

while nRunsCum<nRunsMax:

	paramGridValues = [] #resetting grid values from last loop
	rewardMeanRecord = [] #resetting record of rewards from last loop

	for i in range(0,len(myParams.paramList)):
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,myParams.paramList[i],render=False)]
		nRunsCum +=nRunsAvg
		print "total runs: ", nRunsCum
		print "mean reward of last set: ", rewardMeanRecord[-1]

	numberOfHits = sum(rewardMeanRecord>min(rewardMeanRecord))

	if max(rewardMeanRecord)>bestReward and numberOfHits>0:
		bestReward = max(rewardMeanRecord)
		bestParams = myParams.paramList[rewardMeanRecord.index(max(rewardMeanRecord))]
		print "best average reward:", bestReward
		print "best params: ", bestParams
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,render=True)] #run to show off

		myParams.singleOrderSweep(bestParams) #setting new tighter grid around 'best' values


rewardMeanRecord = [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,render=True)] #run to show off
print "************"
print "best average reward:", bestReward
print "best params: ", bestParams

env.render(close=True)
