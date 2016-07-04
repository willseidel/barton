#priority 1: balancing (move to stop tipping) UNLESS
#priority 2: if we are close to the edge we will reverse direction 

import numpy as np
import gym
env 	= gym.make('CartPole-v0')
#env.monitor.start('/tmp/OpenAI-CartPole', force=True)

nSteps 	= 5000
nRuns 	= 10000
render 	= False
nRunsAvg= 100 #print average reward over the last 'nRunsAvg' runs
aggression = 0.99


bestReward = 0
reward_record = [] #array to hold all rewards

#parameters we optimize
param_x = 2
param_omega = 0.1			
param_omegadot = 0.1


for j in range(nRuns): #looping through simulations

	observation = env.reset()

	reward_cum = 0

	#setting parameters
	param_x_last = param_x
	param_omega_last = param_omega
	param_omegadot_last = param_omegadot


	param_x = param_x_last*(1 + np.random.uniform(-aggression,aggression))
	param_omega = param_omega_last*(1 + np.random.uniform(-aggression,aggression))
	param_omegadot = param_omegadot_last*(1 + np.random.uniform(-aggression,aggression))

	for i in range(nSteps): #looping through time in each simulation


		#basing on angle
		if observation[3]<0:
			action = 0
		else:
			action = 1

		#maybe override based on location

		#if near low edge
		if observation[0]<(env.observation_space.low[0] + param_x): 
			action = 0 #push that direction to get opposite lean
			if (observation[2]>param_omega) or (observation[3]>param_omegadot):
				action = 1 #if we have obtained opposite ean and lean rate

		#if near high edge	
		if observation[0]>(env.observation_space.high[0] - param_x):
			action = 1 #push that direction to get opposite lean
			if (observation[2]<-param_omega) or (observation[3]<-param_omegadot):
				action = 0 #if we have obtained opposite lean and lean rate

		observation, reward, done, info  = env.step(action)
		
		if done:
			break

		reward_cum+=reward

		if render:
			env.render()


	reward_record += [reward_cum]

	avgReward = sum(reward_record[j-(nRunsAvg-1):j])/nRunsAvg
	print "last ", nRunsAvg, " average reward: ",avgReward

	if reward_cum>bestReward:
		bestReward = reward_cum
		#print "last reward: ", reward_cum
	else:
		#print "last reward: ", reward_cum		
		param_x = param_x_last
		param_omega = param_omega_last
		param_omegadot = param_omegadot_last

	print "best reward: ", bestReward
	print "param_x: ", param_x
	print "param_omega: ", param_omega 
	print "param_omegadot: ", param_omegadot 

#env.monitor.close()