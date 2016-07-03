#state: x, x_dot, theta, theta_dot

import gym
import numpy as np
env = gym.make('CartPole-v0')
def eval(env,w,render=False,steps = 200):
    observation = env.reset()
    cum_reward = 0.0        #WHS: resetting cum reward counter?
    for i in range(steps):
        if render:
            env.render()
        w_sum = np.sum(w*observation)
        action = 1 if w_sum > 0 else 0
        observation, reward, done, info = env.step(action)
        cum_reward += reward
        if done:
            break
    return cum_reward

#searching for the best cumulative reward across random configurations
w_hat = None # best model
best_reward = 0.0
for i_episode in range(1):
    w = np.random.rand(1,4) #WHS: make random model parameters
    cum_reward = eval(env,w) #WHS: evaluate model w/random model parameters
    if cum_reward > best_reward:
            best_reward = cum_reward
            w_hat = w

#WHS: once that model is found - we run a single instance of that model?
print("The best reward is {}".format(best_reward))
print(w_hat)
env.monitor.start('/tmp/cartpole-experiment-1',force=True)
eval(env,w_hat,render=True,steps = 1000)
env.monitor.close()