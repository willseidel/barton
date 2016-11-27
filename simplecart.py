#priority 1: balancing (move to stop tipping) UNLESS
#priority 2: if we are close to the edge (or heading there) we will will try to tip towards the middle

import numpy as np
import gym

#the environment
env 			= gym.make('CartPole-v0')

#inputs
nSteps 			= 5000
nRuns 			= 10000
render 			= True
nRunsAvg 		= 100 #print average reward over the last 'nRunsAvg' runs
aggression 		= 0.99

#initializing other variables
bestReward 		= 0
rewardRecord 	= [] #array to hold all rewards

#parameters we optimize
params 			= [10,10,10,10]
paramsBest 		= params[:]


for j in range(nRuns): #looping through simulations

	observation = env.reset()

	reward_cum = 0

	for i in range(nSteps): #looping through time in each simulation


		#basing on angle
		if observation[3]<0:
			action = 0
		else:
			action = 1

		#maybe override based on location

		#if near low edge or heading there fast
		if observation[0]<(env.observation_space.low[0] + params[0]) or observation[1]<-params[1]: 
			action = 0 #push that direction to get opposite lean
			if (observation[2]>params[2]) or (observation[3]>params[3]):
				action = 1 #if we have obtained opposite ean and lean rate

		#if near high edge	or heading there fast
		if observation[0]>(env.observation_space.high[0] - params[0]) or observation[1]>params[1]:
			action = 1 #push that direction to get opposite lean
			if (observation[2]<-params[2]) or (observation[3]<-params[3]):
				action = 0 #if we have obtained opposite lean and lean rate

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
	print "params[0]: ", params[0]
	print "params[1]: ", params[1]
	print "params[2]: ", params[2] 
	print "params[3]: ", params[3] 
	print "paramsBest[0]: ", paramsBest[0]
	print "paramsBest[1]: ", paramsBest[1]
	print "paramsBest[2]: ", paramsBest[2] 
	print "paramsBest[3]: ", paramsBest[3] 

	print "\n"
	#testing if we beat the last set of runs and if so, then using new params
	if (j%nRunsAvg == 0) and j>0:
		if avgReward>bestReward:
			print "new best parameters!"
			bestReward = avgReward
			paramsBest = params[:]

		#setting parameters based on random
		params[0] = paramsBest[0]*(1 + np.random.uniform(-aggression,aggression))
		params[1] = paramsBest[1]*(1 + np.random.uniform(-aggression,aggression))
		params[2] = paramsBest[2]*(1 + np.random.uniform(-aggression,aggression))
		params[3] = paramsBest[3]*(1 + np.random.uniform(-aggression,aggression))


#env.monitor.close()