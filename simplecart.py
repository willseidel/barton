import numpy as np
import gym
env 	= gym.make('CartPole-v0')

nSteps 	= 100
nRuns 	= 5
render 	= False

parameter = 1 
best_reward = 0

for j in range(nRuns): #looping through simulations

	observation = env.reset()

	reward_cum = 0

	for i in range(nSteps): #looping through time in each simulation

		if np.random.uniform(-1,1)<0:
			action = 1
		else:
			action = 0
			
		observation, reward, done, info  = env.step(action)
		
		reward_cum+=reward

		if render:
			env.render()



	if reward_cum>best_reward:
		best_reward = reward_cum



print reward_cum
