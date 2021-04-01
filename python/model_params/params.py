# 4 tesla v100 running on Cuda 9 and CudNN v7
GPU_number = 1
device = 'cpu'

# Hyperparameters - training batch size is mandatory !
batch_norm_decay = 0.9
batch_size = 32
drop_probability = 0.9
early_stop = 50000 #Stops times after no improvement on test set
learning_rate = 1e-4

# Load the graph data
with open('../model_utils/data.pickle', 'rb') as f:
    data = pickle.load(f)

# Store graph data into variables
adj_matrix = tf.constant(data.get('adj'), dtype = tf.float32)
sym_norm = tf.constant(data.get('prod_matrix'), dtype = tf.float32)
number_of_nodes = data.get('number_of_nodes')
number_of_features_per_node = 3


x_size = number_of_nodes * number_of_features_per_node
y_size = number_of_nodes

# Graph architecture
graph_layers = [3,100,100,100,100,100,100]
