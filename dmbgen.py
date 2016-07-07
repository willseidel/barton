#priority 1: balancing (move to stop tipping) UNLESS
#priority 2: if we are close to the edge (or heading there) we will will try to tip towards the middle

import numpy as np
import gym

#the environment
env 			= gym.make('CartPole-v0')

#inputs
nSteps 			= 500
nRuns 			= 50000
render 			= False
renderIfImprove = False #render if it looks like we are about to set a new best
nRunsAvg 		= 10 #print average reward over the last 'nRunsAvg' runs
aggression 		= [100]

#initializing other variables
justImproved 	= False
bestReward 		= [-9e9]
rewardRecord 	= [] #array to hold all rewards
actionOptions 	= []
params 			= [] #parameters we will optimize
dotSpaceMax		= 1 #this is the magnitude that will govern the binning of actions based...
divs			= []	

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

paramsBest 		= params[:]

for j in range(nRuns): #looping through simulations

	if len(bestReward)>1 and justImproved==True: #scale aggression based on relative improvement
		if len(bestReward)>2:
			aggression += ([aggression[-1]*(aggression[-2]/(bestReward[-2] - bestReward[-3]))/(aggression[-1]/(bestReward[-1] - bestReward[-2]))])
		else:
			aggression += [1]
	justImproved = False


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
		
		if done:
			break

		reward_cum+=reward

		if render and j%nRunsAvg==0:
			env.render()
		if renderIfImprove and ((j+1)%nRunsAvg==0) and (avgReward>bestReward[-1]):
			print "avg reward: ",avgReward
			print "best reward: ",bestReward[-1]
			print "run number: ",j
			env.render()

	rewardRecord += [reward_cum]

	avgReward = sum(rewardRecord[-(nRunsAvg+1):-1])/nRunsAvg
	print "run#: ",j
	print "reward: ", reward_cum
	print "last ", nRunsAvg, " average reward: ",avgReward
	print "best reward: ", bestReward[-1]
	print "params: ", params
	print "best params: ", paramsBest
	print "dotSpaceMax: ", dotSpaceMax
	print "aggression: ", aggression[-1]

	print "\n"
	#testing if we beat the last set of runs and if so, then using new params
	if (j%nRunsAvg == 0) and j>0:
		if avgReward>bestReward[-1]:
			print "new best parameters!"
			bestReward 		+= [avgReward]
			paramsBest 		= params[:]
			if len(bestReward)>1:
				justImproved 	= True

		#setting parameters based on random
		for m in range(0,len(params)):
			params[m] = paramsBest[m]*np.exp(np.random.uniform(-aggression[-1],aggression[-1]))

#env.monitor.close()