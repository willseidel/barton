#priority 1: balancing (move to stop tipping) UNLESS
#priority 2: if we are close to the edge we will reverse direction 

import numpy as np
import gym
env 	= gym.make('CartPole-v0')
env.monitor.start('/tmp/OpenAI-CartPole', force=True)

nSteps 	= 1000
nRuns 	= 2
render 	= True

param_x = 2.2 
param_omega = 0.1			
param_omegadot = 0.1

best_reward = 0

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

		#if near low edge
		if observation[0]<(env.observation_space.low[0] + param_x): 
			action = 0 #push that direction to get opposite lean
			if observation[3]>param_omega:
				action = 1 #if we have obtained opposite lean

		#if near high edge	
		if observation[0]>(env.observation_space.high[0] - param_x):
			action = 1 #push that direction to get opposite lean
			if observation[3]<-param_omega:
				action = 0 #if we have obtained opposite lean

		observation, reward, done, info  = env.step(action)
		
		if done:
			break

		reward_cum+=reward

		if render:
			env.render()

	if reward_cum>best_reward:
		best_reward = reward_cum

print reward_cum
env.monitor.close()