#priority 1: balancing (move to stop tipping) UNLESS
#priority 2: if we are close to the edge (or heading there) we will will try to tip towards the middle

import numpy as np
import gym

#the environment
env 			= gym.make('MountainCar-v0')

#inputs
nSteps 			= 300
nRuns 			= 5000
render 			= True
nRunsAvg 		= 100 #print average reward over the last 'nRunsAvg' runs
aggression 		= 100

#initializing other variables
bestReward 		= -9e10
rewardRecord 	= [] #array to hold all rewards
actionOptions 	= []
params 			= [] #parameters we will optimize
dotSpaceMax		= 1 #this is the magnitude that will govern the binning of actions based...
#on the dot product of params and observations. Also optimized
#dotSpaceMaxBest = dotSpaceMax
divs			= []

#this section just finds the range of discrete actions
for i in range(100):
	actionSample = env.action_space.sample() #getting sample
	if actionSample not in actionOptions:
		actionOptions += [actionSample]

nAcs = len(actionOptions)

nObs = len(env.observation_space.sample()) #number of observations


#parameters we optimize
for i in range(0,nObs):
	params += [1]

paramsBest 		= params[:]

for j in range(nRuns): #looping through simulations

	observation = env.reset()

	reward_cum = 0
	divs = []
	#finding where to set bin divisions for assigning actions
	if nAcs ==2: #special case
		divs = [0]
	else: #
		for i in range(1,nAcs):
			divs += [dotSpaceMax - (i-1)*((2*dotSpaceMax)/(nAcs-2))]

	for i in range(nSteps): #looping through time in each simulation

		####INSERT LOGIC
		action = 999
		obsDot = np.dot(params,observation)
		for k in range(0,nAcs-1):
			#print "k:",k
			if obsDot>divs[k]:
				action = actionOptions[k]
				break
			else:
				action = actionOptions[k+1]

		#print "obsdotparams: ",obsDot
		#print "action:", action
		
		#######^^^^^^##############

		observation, reward, done, info  = env.step(action)
		
		if done:
			break

		reward_cum+=reward

		if render:
			if j%nRunsAvg==0:
				env.render()


	rewardRecord += [reward_cum]

	avgReward = sum(rewardRecord[j-(j%nRunsAvg)-1:j])/(j%nRunsAvg+1)
	print "run#: ",j
	print "reward: ", reward_cum
	print "last ", nRunsAvg, " average reward: ",avgReward
	print "best reward: ", bestReward
	print "params: ", params
	print "best params: ", paramsBest
	print "dotSpaceMax: ", dotSpaceMax
	#print "best dotSpaceMax: ", dotSpaceMaxBest

	print "\n"
	#testing if we beat the last set of runs and if so, then using new params
	if (j%nRunsAvg == 0) and j>0:
		if avgReward>bestReward:
			print "new best parameters!"
			bestReward 		= avgReward
			paramsBest 		= params[:]
			#dotSpaceMaxBest = dotSpaceMax

		#setting parameters based on random
		for m in range(0,len(params)):
			params[m] = paramsBest[m]*(1 + np.random.uniform(-aggression,aggression))
			#dotSpaceMax = max(1e-6,dotSpaceMaxBest*(1 + np.random.uniform(-aggression,aggression)))

#env.monitor.close()