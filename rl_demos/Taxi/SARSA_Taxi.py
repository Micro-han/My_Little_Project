import gym
import random


# Q(s_t, a_t) = Q(s_t, a_t) + alpha * [r_t + gamma * Q(n_s, n_a) - Q(s_t, a_t) ]
env = gym.make('Taxi-v3')

alpha = 0.85
gamma = 0.90
epsilon = 0.8
n_epoch = 8000

q = {}
for s in range(env.observation_space.n):
    for a in range(env.action_space.n):
        q[(s, a)] = 0.0


def epsilon_greedy(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return max(list(range(env.action_space.n)), key=lambda x: q[(state, x)])


if __name__ == '__main__':
    for i in range(n_epoch):
        r = 0
        state = env.reset()
        action = epsilon_greedy(state)
        while True:
            next_state, reward, done, info = env.step(action)
            next_aciton = epsilon_greedy(next_state)
            q[(state, action)] += alpha * (reward + gamma * q[(next_state, next_aciton)] - q[(state, action)])
            action = next_aciton
            state = next_state
            r += reward
            if done:
                break
        print('%dth epoch reward is: %d' % (i, r))
    env.close()