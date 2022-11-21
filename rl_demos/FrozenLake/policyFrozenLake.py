import gym
import numpy as np

env = gym.make('FrozenLake-v1')


def compute_value_function(policy, gamma=1.0):
    value_table = np.zeros(4*4)
    threshold = 1e-10
    while True:
        updated_value_table = np.copy(value_table)
        for state in range(4*4):
            action = policy[state]
            value_table[state] = sum([trans_prob * (reward_prob + gamma * updated_value_table[next_state])
                                      for trans_prob, next_state, reward_prob, _ in env.P[state][action]])
        if np.sum(np.fabs(updated_value_table - value_table)) <= threshold:
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


def policy_iteration(gamma=1.0):
    random_policy = np.zeros(env.observation_space.n)
    no_of_iterations = 200000
    for i in range(no_of_iterations):
        new_value_function = compute_value_function(random_policy, gamma)
        new_policy = extract_policy(new_value_function, gamma)
        if np.all(random_policy == new_policy):
            print('Policy-Iteration converged at step %d.' % (i + 1))
            break
        random_policy = new_policy
    return random_policy


if __name__ == "__main__":
    print(policy_iteration(gamma=1.0))