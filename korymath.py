import gym
env = gym.make('CartPole-v0')
env.reset()
env.render()

env.monitor.start('/tmp/reacher-1', force=True)
for i_episode in xrange(101):
    observation = env.reset()
    for t in xrange(100):
        env.render()
        # print observation

        # action selection
        action = env.action_space.sample()

        # take the action and observe the reward and next state
        observation, reward, done, info = env.step(action)

        if done:
            print "Episode finished after {} timesteps".format(t+1)
            break

env.monitor.close()