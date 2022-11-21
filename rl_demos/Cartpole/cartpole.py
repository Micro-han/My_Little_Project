import random

import gym
import numpy as np
import torch
import torch.nn as nn


env = gym.make("CartPole-v0")
experience = []
batch_size = 32
train_episodes = 500
explore_episodes = 100
initial_epsilon = 1.0
gamma = 1.0
final_epsilon = 0.01
learning_rate = 1e-3


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 2)
        )

    def forward(self, x):
        y = self.net(x)
        return y

    def get_action(self, x):
        x = self.forward(x)
        y = torch.argmax(x, 1).numpy()
        return y


if __name__ == '__main__':
    model = Net()
    optimizer = torch.optim.Adam(learning_rate=learning_rate)
    for i in range(train_episodes):
        state = env.reset()
        epsilon = max(initial_epsilon * (train_episodes - i) / train_episodes,final_epsilon)
        step = 0
        while True:
            step = step + 1
            env.render()
            if random.random() < epsilon:
                action = env.action_space.sample()
            else:
                action = model.get_action(np.expand_dims(state, 0)[0])
            next_state, reward, done, info = env.step(action)
            reward = -10 if done else reward
            experience.append((state, action, next_state, reward, 0 if done else 1))
            state = next_state
            if done:
                print("episode %d, epsilon %f, step %d" % (i, epsilon, step))
                break
            if len(experience) >= batch_size:
                batch_state, batch_action, batch_next_state, batch_reward, batch_flag = zip(*random.sample(experience, batch_size))
                batch_state = np.array([s for s in batch_state])
                batch_action = np.array([s for s in batch_action])
                batch_next_state = np.array([s for s in batch_next_state])
                batch_reward = np.array([s for s in batch_reward])
                batch_flag = np.array([s for s in batch_flag])
                Y = np.array(model(batch_next_state))
                Y = batch_reward + (gamma * torch.max)
                Y = batch_reward + \
                    (gamma * tf.reduce_max(Y, axis=1) * batch_flag)
                with tf.GradientTape() as tape:
                    y_pred = tf.reduce_sum(model(batch_state) * tf.one_hot(batch_action, depth=2), axis=1)
                    loss = tf.keras.losses.mean_squared_error(y_true=Y, y_pred=y_pred)
                grads = tape.gradient(loss, model.variables)
                optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))