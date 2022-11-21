import numpy as np
import gym
import tensorflow.compat.v1 as tf
from collections import deque, Counter
import random
import time
from datetime import datetime
tf.disable_eager_execution()

tf.reset_default_graph()
color = np.array([210, 164, 74]).mean()


def pre_process_observation(obs):
    # 预处理图像 将其转换到 88*80的灰度图
    img = obs[1:176:2, ::2]
    img = img.mean(axis=2)
    img[img == color] = 0
    img = (img - 128) / 128 - 1
    return img.reshape(88, 80, 1)


def q_network(X, name_scope, n_output):
    initializer = tf.variance_scaling_initializer()
    with tf.variable_scope(name_scope) as scope:
        # 初始化卷积层
        layer_1 = tf.layers.conv2d(X, filters=32, kernel_size=(8, 8), strides=4, padding='SAME', bias_initializer=initializer)
        # 输出一个直方图
        tf.summary.histogram('layer_1', layer_1)
        layer_2 = tf.layers.conv2d(layer_1, filters=64, kernel_size=(4, 4), strides=2, padding='SAME', bias_initializer=initializer)
        tf.summary.histogram('layer_2', layer_2)
        layer_3 = tf.layers.conv2d(layer_2, filters=64, kernel_size=(3, 3), strides=1, padding='SAME', bias_initializer=initializer)
        tf.summary.histogram('layer_3', layer_3)
        # 馈入连接层时 将layer3结果扁平化
        flat = tf.layers.flatten(layer_3)
        # 全连接层
        fc = tf.layers.dense(flat, units=128, bias_initializer=initializer)
        tf.summary.histogram('fc', fc)
        output = tf.layers.dense(fc, units=n_output, bias_initializer=initializer)
        tf.summary.histogram('output', output)

        # vars变量将保存网络参数
        var_s = {v.name[len(scope.name):]: v for v in tf.get_collection(key=tf.GraphKeys.TRAINABLE_VARIABLES, scope=scope.name)}
        return var_s, output


epsilon = 0.5
eps_min = 0.05
eps_max = 1.0
eps_decay_steps = 500000


def epsilon_greedy(action, step):
    # epsilon 贪心
    p = np.random.random(1).squeeze()
    epsilon = max(eps_min, eps_max - (eps_max-eps_min) * step/eps_decay_steps)
    if np.random.rand() < epsilon:
        return np.random.randint(n_outputs)
    else:
        return action


buffer_len = 20000
exp_buffer = deque(maxlen=buffer_len)


def sample_memories(batch_size):
    # 初始化经验回放缓存
    perm_batch = np.random.permutation(len(exp_buffer))[:batch_size]
    mem = np.array(exp_buffer)[perm_batch]
    return mem[:, 0], mem[:, 1], mem[:, 2], mem[:, 3], mem[:, 4]


if __name__ == '__main__':
    env = gym.make("MsPacman-v0")
    n_outputs = env.action_space.n
    num_episodes = 800
    batch_size = 48
    input_shape = (None, 88, 80, 1)
    learning_rate = 0.001
    X_shape = (None, 88, 80, 1)
    discount_factor = 0.97

    global_step = 0
    copy_steps = 100
    steps_train = 4
    start_steps = 2000

    log_dir = 'logs'
    tf.reset_default_graph()
    X = tf.placeholder(tf.float32, shape=X_shape)
    in_training_mode = tf.placeholder(tf.bool)
    main_q, main_q_outputs = q_network(X, 'mainQ', n_outputs)
    target_q, target_q_outputs = q_network(X, 'targetQ', n_outputs)
    X_action = tf.placeholder(tf.int32, shape=(None, ))
    Q_action = tf.reduce_sum(target_q_outputs * tf.one_hot(X_action, n_outputs), axis=-1, keep_dims=True)
    copy_op = [tf.assign(main_name, target_q[var_name])for var_name, main_name in main_q.items()]
    copy_target_to_main = tf.group(*copy_op)

    y = tf.placeholder(tf.float32, shape=(None, 1))
    loss = tf.reduce_mean(tf.square(y - Q_action))

    optimizer = tf.train.AdamOptimizer(learning_rate)
    training_op = optimizer.minimize(loss)
    loss_summary = tf.summary.scalar('LOSS', loss)
    merge_summary = tf.summary.merge_all()
    file_writer = tf.summary.FileWriter(log_dir, tf.get_default_graph())
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        init.run()
        for i in range(num_episodes):
            done = False
            obs = env.reset()
            epoch = 0
            episodic_reward = 0
            actions_counter = Counter()
            episodic_loss = []
            while not done:
                obs = pre_process_observation(obs)
                actions = main_q_outputs.eval(feed_dict={X: [obs], in_training_mode: False})
                action = np.argmax(actions, axis=-1)
                actions_counter[str(action)] += 1
                action = epsilon_greedy(action, global_step)
                next_obs, reward, done, _ = env.step(action)
                exp_buffer.append([obs, action, pre_process_observation(next_obs), reward, done])
                if global_step % steps_train == 0 and global_step > start_steps:
                    o_obs, o_act, o_next_obs, o_rew, o_done = sample_memories(batch_size)
                    o_obs = [x for x in o_obs]
                    o_next_obs = [x for x in o_next_obs]
                    next_act = main_q_outputs.eval(feed_dict={X: o_next_obs, in_training_mode: False})
                    y_batch = o_rew + discount_factor * np.max(next_act, axis=-1) * (1 - o_done)
                    mrg_summary = merge_summary.eval(feed_dict={X: o_obs, y: np.expand_dims(y_batch, axis=-1), X_action: o_act, in_training_mode: False})
                    file_writer.add_summary(mrg_summary, global_step)
                    training_loss, _ = sess.run([loss, training_op], feed_dict={X: o_obs, y: np.expand_dims(y_batch, axis=-1), X_action: o_act, in_training_mode: True})
                    episodic_loss.append(training_loss)
                if (global_step + 1) % copy_steps == 0 and global_step > start_steps:
                    copy_target_to_main.run()
                obs = next_obs
                epoch += 1
                global_step += 1
                episodic_reward += reward
            print('Epoch', epoch, 'Reward', episodic_reward,)