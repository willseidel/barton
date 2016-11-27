import numpy as np

def evalParamSet(env,nRuns,divs,nAcs,params,nSteps,actionOptions,render):
	#this function runs nRuns simulations using a set of parameters to evaluate
	#the highest reward that the parameter set produces

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