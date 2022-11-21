import gym
import numpy as np


# 创建环境
env = gym.make('FrozenLake-v1')


def value_iteration(gamma=1.0):
    # 初始化
    value_table = np.zeros(env.observation_space.n)
    no_of_iteration = 100000
    threshold = 1e-20
    # 开始迭代
    for i in range(no_of_iteration):
        updated_value_table = np.copy(value_table)
        for state in range(env.observation_space.n):
            q_value = []
            for action in range(env.action_space.n):
                next_state_rewards = []
                for next_sr in env.P[state][action]:
                    trans_prob, next_state, reward_prob, _ = next_sr
                    next_state_rewards.append((trans_prob * (reward_prob + gamma * updated_value_table[next_state])))
                q_value.append(np.sum(next_state_rewards))
            value_table[state] = max(q_value)
        if np.sum(np.fabs(updated_value_table - value_table)) <= threshold:
            print('Value-iteration converged at iteration# %d.' % (i + 1))
            break
    return value_table


def extract_policy(value_table, gamma=1.0):
    policy = np.zeros(env.observation_space.n)
    for state in range(env.observation_space.n):
        q_table = np.zeros(env.action_space.n)
        for action in range(env.action_space.n):
            for next_sr in env.P[state][action]:
                trans_prob, next_state, reward_prob, _ = next_sr
                q_table[action] += (trans_prob * (reward_prob + gamma * value_table[next_state]))
        policy[state] = np.argmax(q_table)
    return policy


def main():
    env.reset()
    # env.render()
    optimal_value_function = value_iteration(gamma=1.0)
    optimal_policy = extract_policy(optimal_value_function, gamma=1.0)
    print(optimal_policy)


if __name__ == "__main__":
    main()