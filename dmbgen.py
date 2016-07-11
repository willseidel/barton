#1) define grid of parameter sets...run through that grid w/nRunsAvg per set
#2) find the best parameter set
#3) define a new grid at tighter order centered on those values - goto #1

import numpy as np
import gym


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
			if render:
				env.render()
			if done:
				break

			reward_cum += reward


		rewardRecord += [reward_cum]
		print "run#: ",j
		print "reward: ", reward_cum
		print "params: ", params
		print "\n"


	#meanReward =  np.mean(rewardRecord)
	#return meanReward
	return np.mean(rewardRecord)

def paramSweep(paramVals,nSet):

	nGuessVal 	= len(paramVals)
	nComb 		= nGuessVal**nSet
	paramList 		= np.zeros((nComb,nSet))

	for i in range(0,nComb):
		for j in range(0,nSet):
				valIndex = (int(np.floor(i/(nGuessVal**(nSet - j - 1)))))%nGuessVal
				paramList[i][j] = paramVals[valIndex]

	return paramList


#the environment
env 			= gym.make('MountainCar-v0')

#inputs
nSteps 			= 5000
nRunsAvg 		= 1


#initializing other variables
render 			= False
actionOptions 	= []
params 			= [] #parameters we will optimize
dotSpaceMax		= 1 #this is the magnitude that will govern the binning of actions based...
divs			= []	
paramGridOrder	= 6 #search grid will go up/down by this many orders of magnitude

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

##########SCRATCH FOR LOOPING THROUGH GRID
rewardMeanRecord = []
paramGridValues = []

for i in range(0,paramGridOrder):
	paramGridValues += [10**i]
	paramGridValues += [-10**i]

paramSet = paramSweep(paramGridValues,len(params))

for i in range(0,len(paramSet)):
	rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,paramSet[i],render)]

bestParams = paramSet[rewardMeanRecord.index(max(rewardMeanRecord))]



