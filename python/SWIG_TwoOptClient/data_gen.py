#Use of Thomas Kipf's kernel (2016)
#Optimized with the use of CudNN  v7 for the Tesla V100 GPUs in the DGX-station - use of CudNN v6 will cause loss of performance
#Requires python3 for average_gradients function
#Updated on 20/02/2018
import numpy as np
import h5py

exec(open("./../input/graph.py").read())

adj_matrix = np.asarray(A)

f1 = h5py.File("../model_utils/raw_data.hdf5", "w")
d1 = f1.create_dataset('raw', (10**8, x_size + y_size),
maxshape=(None, x_size + y_size), dtype='i')

# Hyperparameters
exec(open("./implementation_A_star_contrained_nodes.py").read())


adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary = adj_matrix_creator(adj_matrix)
g = SimpleGraph(adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary)
number_of_processed_examples = 0

for i in range(number_of_nodes):

	start = i
	goal = i
	mandatories = []
	#max_iter = 500
	start_time = time.time()
	print("i = %d, BEFORE : %d "%(i,number_of_processed_examples))
	result = a_star_search(g, start, goal, mandatories, number_of_processed_examples)

	if result != False:
		[cost, total_cost, num, last_mandatory_point, number_of_processed_examples] = result
		#print("\n The optimal path is: %s"%path[1])
		#print("\n The cost is: %f"%total_cost)
		print("\n Number of visits: %f"%num)
		#print("\n Last mandatory points: %s"%last_mandatory_point)
		print("--- %s seconds ---" % (time.time() - start_time))

	else:
		print("\n No path found")
	print("i = %d, AFTER : %d "%(i,number_of_processed_examples))

d1.resize(number_of_processed_examples, axis=0)
f1.close()
