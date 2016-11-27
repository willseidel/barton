#this is the front end script that:
#1) figures out how many actions an environment has
#2) creates a grid of parameters to evaluate
#3) evalutes those parameters to find a best hit
#4) refines the grid
#5) continues evaluating and refining
#6) shows the final result
##########
#This file relies on 
# - evalParamSet.py
# - paramSet.py

from paramSet import paramSet
from evalParamSet import evalParamSet
import numpy as np
import gym


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
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,myParams.paramList[i],nSteps,actionOptions,render=False)]
		nRunsCum +=nRunsAvg
		print "total runs: ", nRunsCum
		print "mean reward of last set: ", rewardMeanRecord[-1]

	numberOfHits = sum(rewardMeanRecord>min(rewardMeanRecord))

	if max(rewardMeanRecord)>bestReward and numberOfHits>0:
		bestReward = max(rewardMeanRecord)
		bestParams = myParams.paramList[rewardMeanRecord.index(max(rewardMeanRecord))]
		print "best average reward:", bestReward
		print "best params: ", bestParams
		rewardMeanRecord += [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,nSteps,actionOptions,render=True)] #run to show off

		myParams.singleOrderSweep(bestParams) #setting new tighter grid around 'best' values


rewardMeanRecord = [evalParamSet(env,nRunsAvg,divs,nAcs,bestParams,nSteps,actionOptions,render=True)] #run to show off
print "************"
print "best average reward:", bestReward
print "best params: ", bestParams

env.render(close=True)