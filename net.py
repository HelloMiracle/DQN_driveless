import tensorflow as tf
import numpy as np
import random
from collections import deque

gamma = 0.999 # 折扣奖励系数
initial_epsilon = 0.5 # 初始随机因子
final_epsilon = 0.01 #终止随机因子
replay_size = 600000 # 经验存储空间大小
batch_size = 32 # 微训练集大小

class dqn():
    def __init__(self):
        self.replay_buffer = deque()
        self.times = 0
        self.time_step = 0
        self.epsilon = initial_epsilon
        self.state_dim = 6
        self.action_dim = 2

        self.create_Q_network()
        self.create_training_method()

        self.session = tf.InteractiveSession()
        self.session.run(tf.global_variables_initializer())
        
    def create_Q_network(self):
        w1 = self.weight_variable([self.state_dim, 120])
        b1 = self.bias_variable([120])
        w2 = self.weight_variable([12, self.action_dim])
        b2 = self.bias_variable([self.action_dim])
        w3 = self.weight_variable([120,12])
        b3 = self.bias_variable([12])


        self.state_input = tf.placeholder("float", [None, self.state_dim])

        h_layer = tf.nn.relu(tf.matmul(self.state_input, w1) + b1)

        h_layer2 = tf.nn.relu(tf.matmul(h_layer, w3) + b3)
        
        self.q_value = tf.matmul(h_layer2, w2) + b2
        
        self.saver = tf.train.Saver()
        

    def create_training_method(self ):
        self.action_input = tf.placeholder("float", [None, self.action_dim])
        self.y_input = tf.placeholder("float", [None])
        q_action = tf.reduce_sum(tf.multiply(self.q_value, self.action_input), reduction_indices = 1)
        self.cost = tf.reduce_mean(tf.square(self.y_input - q_action))
        self.optimizer = tf.train.AdamOptimizer(0.0001).minimize(self.cost)

    def preceive(self, state, action, reward, next_state, done):
        one_hot_action = np.zeros(self.action_dim)
        one_hot_action[action] = 1
        self.replay_buffer.append((state, one_hot_action, reward, next_state, done))
        if len(self.replay_buffer)  > replay_size:
            self.replay_buffer.popleft()
        if len(self.replay_buffer) > batch_size:
            self.train_Q_network()

        
    def save_net(self, path):
        print('successful save')
        saver_path = self.saver.save(self.session, path)

    def restore(self, path):
        print('successful restore' + path)
        self.saver.restore(self.session, path)
        
    def train_Q_network(self):
        self.time_step += 1
        minibatch = random.sample(self.replay_buffer, batch_size)
        state_batch = [data[0] for data in minibatch]
        action_batch = [data[1] for data in minibatch]
        reward_batch = [data[2] for data in minibatch]
        next_state_batch = [data[3] for data in minibatch]

        y_batch = []
        q_value_batch = self.q_value.eval(feed_dict = {self.state_input: next_state_batch})
        for i in range(0, batch_size):
            done = minibatch[i][4]
            if done:
                y_batch.append(reward_batch[i])
            else:
                y_batch.append(reward_batch[i] + gamma * np.max(q_value_batch[i]))


        self.optimizer.run(feed_dict = {
            self.y_input: y_batch,
            self.action_input: action_batch,
            self.state_input: state_batch
            })
        

    def egreedy_action(self, state):
        q_value = self.q_value.eval(feed_dict = {
            self.state_input:[state]
            })[0]
        if self.epsilon > final_epsilon:
            self.epsilon -= (initial_epsilon - final_epsilon)/10000
        else:
            self.epsilon = 0.01
        if random.random() <= self.epsilon:
            return random.randint(0, self.action_dim - 1)
        else:
            return np.argmax(q_value)
        
        

        
    def action(self, state):
        return np.argmax(self.q_value.eval(feed_dict = {
            self.state_input:[state]
            })[0])

    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.constant(0.01, shape = shape)
        return tf.Variable(initial)



print('success dqn')

               

