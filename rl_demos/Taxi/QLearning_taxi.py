import random
import gym


env = gym.make('Taxi-v3')

alpha = 0.4
gamma = 0.99
epsilon = 0.17
n_epoch = 8000

q = {}

for s in range(env.observation_space.n):
    for a in range(env.action_space.n):
        q[(s, a)] = 0


def update_q_table(pre_state, action, reward, next_state):
    q_a = max(q[next_state, a] for a in range(env.action_space.n))
    q[(pre_state, action)] += alpha * (reward + gamma * q_a - q[(pre_state, action)])


def epsilon_greedy_policy(state):
    if random.uniform(0, 1) < epsilon:
        return env.action_space.sample()
    else:
        return max(list(range(env.action_space.n)), key=lambda x: q[state, x])


if __name__ == '__main__':
    for i in range(n_epoch):
        r = 0
        pre_state = env.reset()
        while True:
            action = epsilon_greedy_policy(pre_state)
            next_state, reward, done, info = env.step(action)
            update_q_table(pre_state, action, reward, next_state)
            pre_state = next_state
            r += reward
            if done:
                break
        print("%dth epoch reward is %d" % (i, r))
    env.close()