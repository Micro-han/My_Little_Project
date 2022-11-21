import numpy as np
import gym
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
from functools import partial


plt.style.use('ggplot')
env = gym.make('Blackjack-v1')
print(env.action_space, env.observation_space)


def sample_policy(observation):
    score, dealer_score, usable_ace = observation
    return 0 if score >= 20 else 1


def generate_episode(policy):
    states, actions, rewards = [], [], []
    observation = env.reset()
    while True:
        states.append(observation)
        action = policy(observation)
        actions.append(action)
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        if done:
            break
    return states, actions, rewards


def first_visit_mc_prediction(policy, n_episodes):
    value_table = defaultdict(float)
    n = defaultdict(int)
    for _ in range(n_episodes):
        states, _, rewards = generate_episode(policy)
        returns = 0
        for t in range(len(states) - 1, -1, -1):
            r = rewards[t]
            s = states[t]
            returns = returns + r
            if s not in states[:t]:
                n[s] = n[s] + 1
                value_table[s] = value_table[s] + (returns - value_table[s]) / n[s]
    return value_table


value = first_visit_mc_prediction(sample_policy, n_episodes=500000)
for i in range(0, 10):
    print(value.popitem())


def plot_blackjack(v, ax1, ax2):
    player_sum = np.arange(12, 21 + 1)
    dealer_show = np.arange(1, 10 + 1)
    usable_ace = np.array([False, True])
    state_values = np.zeros((len(player_sum), len(dealer_show), len(usable_ace)))
    for i, player in enumerate(player_sum):
        for j, dealer in enumerate(dealer_show):
            for k, ace in enumerate(usable_ace):
                state_values[i, j, k] = v[player, dealer, ace]
    x, y = np.meshgrid(player_sum, dealer_show)
    ax1.plot_wireframe(x, y, state_values[:, :, 0])
    ax2.plot_wireframe(x, y, state_values[:, :, 1])
    for ax in ax1, ax2:
        ax.set_zlim(-1, 1)
        ax.set_ylabel('Player sum')
        ax.set_xlabel('dealer showing')
        ax.set_zlabel('state-value')
        plt.show()


if __name__ == '__main__':
    fig, axes = pyplot.subplots(nrows=2, figsize=(5, 8), subplot_kw={'projection': '3d'})
    axes[0].set_title('value function without usable ace')
    axes[1].set_title('value function with usable ace')
    plot_blackjack(value, axes[0], axes[1])