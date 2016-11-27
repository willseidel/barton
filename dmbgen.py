#TODO: Make parameter set creation function to increase code reuse.

import numpy as np
import gym



#this function runs nRuns simulations using a set of parameters to evaluate
#the highest reward that the parameter set produces
def evalParamSet(env,nRuns,divs,nAcs,params,render):

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
params 				= [] #parameters we will optimize
dotSpaceMax			= 1 #this is the magnitude that will govern the binning of actions based...
divs				= []	
rewardMeanRecord 	= []
paramGridValues 	= []
bestReward 			= -10e10
nRunsCum 			= 0 #total number of runs

#this section just finds the range of discrete actions
for i in range(100):
	actionSample = env.action_space.sample() #getting sample
	if actionSample not in actionOptions:
		actionOptions += [actionSample]

nAcs = len(actionOptions) #number of actions
nObs = len(env.observation_space.sample()) #number of observation indices

#parameters we optimize
for i in range(0,nObs):
	params += [1]

#finding where to set bin divisions for assigning actions
if nAcs ==2: #special case
	divs = [0]
else: #
	for i in range(1,nAcs):
		divs += [dotSpaceMax - (i-1)*((2*dotSpaceMax)/(nAcs-2))]

for i in range(0,paramGridOrder):
	for k in range(0,paramGridDensity):
		paramGridValues += [((k+1)*(10/paramGridDensity))*(10**i)]
		paramGridValues += [-((k+1)*(10/paramGridDensity))*(10**i)]

paramSet = paramSweep(paramGridValues,len(params))
bestParams = paramSet[1]
while nRunsCum<nRunsMax:

	paramGridValues = [] #resetting grid values from last loop
	rewardMeanRecord = [] #resetting record of rewards from last loop

	for i in range(0,len(paramSet)):
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,paramSet[i],render=False)]
		nRunsCum +=nRunsAvg
		print "total runs: ", nRunsCum
		print "mean reward of last set: ", rewardMeanRecord[-1]

	numberOfHits = sum(rewardMeanRecord>min(rewardMeanRecord))

	if max(rewardMeanRecord)>bestReward and numberOfHits>0:
		bestReward = max(rewardMeanRecord)
		bestParams = paramSet[rewardMeanRecord.index(max(rewardMeanRecord))]
		print "best average reward:", bestReward
		print "best params: ", bestParams
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,render=True)] #run to show off

		for k in range(1,paramGridDensity): #setting new tighter grid around 'best' values
			for l in range(0,len(params)):
				paramGridValues += [(1+(k/10.0))*bestParams[l]]
				paramGridValues += [-(1+(k/10.0))*bestParams[l]]

		paramSet = paramSweep(paramGridValues,len(params)) #new paramSet


rewardMeanRecord = [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,render=True)] #run to show off
print "************"
print "best average reward:", bestReward
print "best params: ", bestParams

env.render(close=True)


print "paramGridDensity: ",paramGridDensity
print "paramGridOrder: ",paramGridOrder
print "len(bestparams): ",len(bestParams)
print "lens(params):", len(params)
