import tensorflow as tf

def weight_init(shape):
    return tf.Variable(tf.truncated_normal(shape,stddev=0.1))
def bias_init(shape):
    return tf.Variable(tf.constant(0.1,shape))

def conv2d(x,w):
    return tf.nn.conv2d(x,w,strides=[1,2,2,1],padding='SAME')

def max_pool(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1])
input=tf.placeholder(tf.float32,[None,28,28,3])
label=tf.placeholder(tf.float32,[None,10])
w_1=weight_init([5,5,1,32])
b_1=bias_init([32])
layer_1=tf.nn.relu(conv2d(input,w_1)+b_1)
max_pool_1=max_pool(layer_1)
