import numpy as np
import gym
env 	= gym.make('CartPole-v0')

nSteps 	= 100
nRuns 	= 5
render 	= True


for j in range(nRuns): #looping through simulations

	observation = env.reset()

	for i in range(nSteps): #looping through time in each simulation

		if np.random.uniform(-1,1)<0:
			action = 1
		else:
			action = 0
		observation, reward, done, info  = env.step(action)
		
		print reward
		if render:
			env.render()


