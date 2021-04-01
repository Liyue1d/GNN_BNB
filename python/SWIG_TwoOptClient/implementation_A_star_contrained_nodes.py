import h5py
import heapq
import random
import collections
import numpy as np
import math
import time



inf_bound = math.pow(10,29)

'''
f1 = h5py.File("../model_utils/raw_data.hdf5", "w")
d1 = f1.create_dataset('my_dataset', (10**7, x_size + y_size),
maxshape=(None, x_size + y_size), dtype='i', chunks=(10**6, x_size + y_size))
'''

def arrayStatetoString(arrayState):
	return "[" + ','.join(list(map(str, arrayState))) + "]"

def stringStatetoArrayState(stringState):
	return list(map(int,stringState.replace("[","").replace("]","").split(",")))

def state_departure_node(arrayState, number_of_nodes):
	for i in range(number_of_nodes):
		if arrayState[i * 3] == 1:
			return i

def state_arrival_node(arrayState, number_of_nodes):
	for i in range(number_of_nodes):
		if arrayState[i * 3 + 1] == 1:
			return i

def state_mandatory_nodes(arrayState, number_of_nodes):
	mandatories = []
	for i in range(number_of_nodes):
		if arrayState[i * 3 + 2] == 1:
			mandatories.append(i)
	return mandatories

def is_goal_state(arrayState, number_of_nodes):
	dep_arr = False
	no_mandatory = True
	for i in range(number_of_nodes):
		if arrayState[i * 3] == 1:
			if arrayState[i * 3 + 1] == 1:
				dep_arr = True
		if arrayState[i * 3 + 2] == 1:
			no_mandatory = False

	return dep_arr and no_mandatory


class SimpleGraph:
	def __init__(self, adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary):
		self.adjacency_matrix_binary = adjacency_matrix_binary
		self.adjacency_cost_matrix_with_upper_bound = adjacency_cost_matrix_with_upper_bound
		self.number_of_nodes = adjacency_matrix_binary.shape[0]

	def neighbors(self, arrayState):
		current_node = state_departure_node(arrayState, self.number_of_nodes)
		arrival_node = state_arrival_node(arrayState, self.number_of_nodes)
		current_mand = state_mandatory_nodes(arrayState, self.number_of_nodes)
		neighbors = np.where(np.squeeze(np.asarray(self.adjacency_matrix_binary[current_node])) == 1)[0]
		neighbor_list = []

		for neighbor_id in neighbors:
			if not neighbor_id in current_mand:
				#Without waypoint added
				neighbor_state = list(arrayState)
				neighbor_state[current_node * 3] = 0
				neighbor_state[neighbor_id * 3] = 1
				neighbor_list.append(arrayStatetoString(neighbor_state))

				#With waypoint added
				neighbor_state = list(arrayState)
				neighbor_state[current_node * 3] = 0
				neighbor_state[neighbor_id * 3] = 1
				if current_node != arrival_node:
					neighbor_state[current_node * 3 + 2] = 1
				neighbor_list.append(arrayStatetoString(neighbor_state))


		return neighbor_list

	def cost(self, current_state, next_state):
		array_current_state = stringStatetoArrayState(current_state)
		array_next_state = stringStatetoArrayState(next_state)
		dep_node = state_departure_node(array_current_state, self.number_of_nodes)
		arr_node = state_departure_node(array_next_state, self.number_of_nodes)

		return adjacency_cost_matrix_with_upper_bound[dep_node, arr_node]

	def getNumberofNodes(self):
		return self.number_of_nodes


class PriorityQueue:
	def __init__(self):
		self.elements = []

	def randItem(self):
		ind = random.randint(0,len(self.elements))
		element = self.elements[ind]
		del self.elements[ind]
		return element

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]



def reconstruct_path(came_from, start, goal, number_of_nodes):

	current = goal
	statePath = []
	nodePath = []

	while current != start:
		statePath.append(current)
		nodePath.append(state_departure_node(stringStatetoArrayState(current), number_of_nodes))
		current = came_from[current]

	statePath.append(start)
	nodePath.append(state_departure_node(stringStatetoArrayState(start), number_of_nodes))

	statePath.reverse()
	nodePath.reverse()

	return [statePath, nodePath]

def heuristic(str_state):
	return 0

def a_star_search(graph, start, goal, mandatories, number_of_processed_examples):
	depth_mand = 0
	number_of_nodes = graph.getNumberofNodes()
	array_start_state = []
	array_goal_state = []
	number_of_visits = 0


	for i in range(number_of_nodes * 3):
		array_start_state.append(0)
		array_goal_state.append(0)

	array_start_state[start * 3] = 1
	array_start_state[goal * 3 + 1] = 1

	for m in mandatories:
		array_start_state[m * 3 + 2] = 1

	array_goal_state[goal * 3] = 1
	array_goal_state[goal * 3 + 1] = 1

	string_start_state = arrayStatetoString(array_start_state)
	string_goal_state = arrayStatetoString(array_goal_state)

	frontier = PriorityQueue()
	frontier.put(string_start_state, 0)
	came_from = {}
	last_mandatory_point = {}
	last_mandatory_point[string_start_state] = ''
	cost_so_far = {}
	came_from[string_start_state] = None
	cost_so_far[string_start_state] = 0

	while not frontier.empty():
		currentStringState = frontier.get()
		number_of_visits += 1

		if number_of_visits > max_iter:
			break

		currentArrayState = stringStatetoArrayState(currentStringState)
		currentStateMandNodes = state_mandatory_nodes(currentArrayState, number_of_nodes)
		list_np_currentArrayState = [np.array(currentArrayState)]
		if len(currentStateMandNodes)>depth_mand:
			depth_mand = len(currentStateMandNodes)
			print("\n reached mand depth %d"%depth_mand)


		if len(currentStateMandNodes) > 0:

			x = np.array(currentArrayState)
			y = np.zeros((number_of_nodes))
			y[last_mandatory_point[currentStringState]]=1
			#print("\n DOING %d"%number_of_processed_examples)
			#print(type(d1[number_of_processed_examples]))
			#print(x)
			#print(y)
			#print(np.concatenate((x, y)))
			d1[number_of_processed_examples] = np.concatenate((x, y))
			number_of_processed_examples += 1

		for next in graph.neighbors(currentArrayState):
			new_cost = cost_so_far[currentStringState] + graph.cost(currentStringState, next)

			if next not in cost_so_far or new_cost < cost_so_far[next]:
				next_array = stringStatetoArrayState(next)
				nextStateMandNodes = state_mandatory_nodes(next_array, number_of_nodes)
				next_dep_node = state_departure_node(next_array, number_of_nodes)
				cost_so_far[next] = new_cost
				priority = new_cost + heuristic(next)
				frontier.put(next, priority)
				came_from[next] = currentStringState
				if len(currentStateMandNodes) == len(nextStateMandNodes):
					last_mandatory_point[next] = last_mandatory_point[currentStringState]
				else:
					last_mandatory_point[next] = state_departure_node(currentArrayState, number_of_nodes)

	if string_goal_state not in came_from:
		return False

	return [cost_so_far, cost_so_far[string_goal_state], number_of_visits, last_mandatory_point, number_of_processed_examples]

def adj_matrix_creator(adjacency_cost_matrix):
	adjacency_matrix_binary = (adjacency_cost_matrix > 0)
	adjacency_cost_matrix_with_upper_bound = adjacency_cost_matrix + inf_bound * (adjacency_cost_matrix == 0)
	return adjacency_cost_matrix_with_upper_bound, adjacency_matrix_binary
