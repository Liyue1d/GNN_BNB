def model(scope, x, y, is_training, batch_norm_decay, dropout_prob,
sym_norm, number_of_nodes, graph_layers):

    #Size of input vector x - number of examples in the batch
    n_size = tf.shape(x)[0]
    #Vectorized sym_norm - replication size(x) number of times
    sym_norm_vect = tf.reshape(tf.tile(sym_norm,[n_size,1]),[n_size, number_of_nodes, number_of_nodes])
    #Creating 3rd dimension. Each example is now a number_of_nodes x 3 matrix
    forward = tf.reshape(x, [n_size, number_of_nodes, number_of_features_per_node])

    #Feedforward
    for i in range(1,len(graph_layers)):

        #Weight variable for layer i
        weight = tf.get_variable(name = "my_variable_%d"%i,
        shape = [graph_layers[i-1],graph_layers[i]], initializer = tf.contrib.layers.xavier_initializer())

        #Vectorized weight variable - replication size(x) number of times
        weight_vect = tf.reshape(tf.tile(weight,[n_size,1]),[n_size, graph_layers[i-1], graph_layers[i]])

        #Graph Convolution
        forward = tf.matmul(tf.matmul(sym_norm_vect,forward), weight_vect)

        forward = tf.contrib.layers.batch_norm(inputs = forward,
        is_training = is_training, decay = batch_norm_decay, updates_collections = None, fused = True, scope = "norm%d"%i)
        forward = tf.nn.relu(forward)


    flattened = tf.reshape(forward, [n_size, number_of_nodes * graph_layers[-1]])

    dropout = tf.contrib.layers.dropout(
    	inputs = flattened,
    	keep_prob=dropout_prob,
    	noise_shape=None,
    	is_training=is_training,
    	outputs_collections=None
    )

    readout = tf.contrib.layers.fully_connected(
    inputs = dropout,
    num_outputs = number_of_nodes,
    activation_fn=None,
    biases_initializer=tf.zeros_initializer(),
    scope = 'full2var')

    prob = tf.nn.softmax (readout)

    losses = tf.reduce_sum(- y * tf.log(tf.clip_by_value(prob,1e-10,1.0)), axis = 1)
    total_loss = tf.reduce_sum(losses, axis = 0)
    average_loss = tf.reduce_mean(losses)

    return prob, total_loss, average_loss

opt = tf.train.AdamOptimizer(learning_rate)

is_training = tf.placeholder(tf.bool)
dropout_prob = tf.placeholder(tf.float32)

x0 = tf.placeholder(tf.float32, shape=[None, x_size])
y0 = tf.placeholder(tf.float32, shape=[None, y_size])

x1 = tf.placeholder(tf.float32, shape=[None, x_size])
y1 = tf.placeholder(tf.float32, shape=[None, y_size])

x2 = tf.placeholder(tf.float32, shape=[None, x_size])
y2 = tf.placeholder(tf.float32, shape=[None, y_size])

x3 = tf.placeholder(tf.float32, shape=[None, x_size])
y3 = tf.placeholder(tf.float32, shape=[None, y_size])

x4 = tf.placeholder(tf.float32, shape=[None, x_size])
y4 = tf.placeholder(tf.float32, shape=[None, y_size])

with tf.variable_scope(tf.get_variable_scope()):

	with tf.name_scope("t0") as scope, tf.device('/%s:0'%device):
		prob0, total_loss0, average_loss0 = model(scope, x0, y0, is_training,
		batch_norm_decay, dropout_prob, sym_norm, number_of_nodes, graph_layers)
		tf.get_variable_scope().reuse_variables()
		tf.summary.scalar('loss', average_loss0)

"""
	with tf.name_scope("t1") as scope, tf.device('/%s:1'%device):
		prob1, total_loss1, average_loss1 = model(scope, x1, y1, is_training,
        batch_norm_decay, dropout_prob, sym_norm, number_of_nodes, graph_layers)
		tf.get_variable_scope().reuse_variables()

	with tf.name_scope("t2") as scope, tf.device('/%s:2'%device):
		prob2, total_loss2, average_loss2 = model(scope,x2, y2, is_training,
        batch_norm_decay, dropout_prob, sym_norm, number_of_nodes, graph_layers)
		tf.get_variable_scope().reuse_variables()

	with tf.name_scope("t3") as scope, tf.device('/%s:3'%device):
		prob3, total_loss3, average_loss3 = model(scope, x3, y3, is_training,
        batch_norm_decay, dropout_prob, sym_norm, number_of_nodes, graph_layers)
		tf.get_variable_scope().reuse_variables()

"""


with tf.device('/%s:0'%device):
	train_0 = opt.minimize(average_loss0)

"""
with tf.device('/%s:1'%device):
	train_1 = opt.minimize(average_loss1)

with tf.device('/%s:2'%device):
	train_2 = opt.minimize(average_loss2)

with tf.device('/%s:3'%device):
	train_3 = opt.minimize(average_loss3)
"""

train_step_single = train_0



correct_prediction = tf.equal(tf.argmax(prob0, 1), tf.argmax(y0, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter('../tensorboard/train')
test_writer = tf.summary.FileWriter('../tensorboard/test')
