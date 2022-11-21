import gym
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn


# 引入环境
env = gym.make("Blackjack-v1")
print(env.observation_space)
# 初始化q表 探索率 在状态s选择动作a概率 累计奖励表
q_table = {}
rate = 0.4
policy = {}
returns = {}


# 生成情景
def generate_episode(q_table, policy):
    episodes = []
    state = env.reset()
    while True:
        # 该状态第一次出现
        if state not in q_table.keys():
            q_table[state] = {0: 0.0, 1: 0.0}
            policy[state] = [0.5, 0.5]
            returns[state] = {0: [], 1: []}
        # 与环境交互 产生奖励
        action = np.random.choice([0, 1], p=policy[state], size=1)[0]
        next_s, reward, done, info = env.step(action)
        episodes.append((state, action, reward))
        if done:
            break
        state = next_s
    return episodes


if __name__ == '__main__':
    # 迭代次数
    n_iter = 500000
    for i in range(n_iter):
        # 对于每一个情景序列
        episode = generate_episode(q_table, policy)
        grate = 0.0
        for j in range(len(episode))[::-1]:
            state, action, reward = episode[j]
            grate += reward
            if (state, action) not in [k[: 2] for k in episode[:j]]:
                returns[state][action].append(grate)
                q_table[state][action] = np.mean(returns[state][action])
            a_star = np.argmax(list(q_table[state].values()))
            policy[state][a_star] = 1 - rate + rate / 2
            policy[state][1 - a_star] = rate / 2

    q_data = pd.DataFrame([list(item.values()) for item in list(q_table.values())], index=list(q_table.keys()), columns=['stick', 'hit'])
    print(q_data)