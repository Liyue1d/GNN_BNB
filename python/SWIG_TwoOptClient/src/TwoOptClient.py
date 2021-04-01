#!/usr/bin/python
import sys
import numpy as np
import networkx as nx
import time

sys.path.append('lib')
from TwoOpt import *

def twoOptCompute(A,instance, upper_bound):

    n = A.shape[0]
    G = nx.from_numpy_matrix(A)

    #Instance to solve
    departure = instance[0]
    arrival = instance[1]
    mandatories = instance[2]
    mand_order = np.array(mandatories).astype(float)

    #Nodes of new graph
    new_nodes = []
    new_nodes.append(departure)
    new_nodes.append(arrival)
    new_nodes.extend(mandatories)
    ngs = len(new_nodes)

    #Adj matrix of new graph
    NA = np.zeros((ngs+1,ngs+1))
    for i in range(ngs):
    	for j in range(ngs):
    		NA[i][j] = nx.dijkstra_path_length(G, new_nodes[i], new_nodes[j])
    #print(" \nMatrix of new graph: \n %s"%NA)
    print(NA)

    #Solver instanciation and run
    solver = TwoOpt()
    inf = np.zeros(3)
    visits_group = np.zeros(20)
    cuts_group = np.zeros(20)
    root_visits_group = np.zeros(20)
    tour_order = np.zeros(ngs+2)
    score_value = np.zeros(20)
    #NA = np.array([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])

    if(upper_bound > 0):
        cost = 0
        cost += nx.dijkstra_path_length(G, departure, mand_order[0]);
        for i in range(mand_order.size - 1):
        	cost += nx.dijkstra_path_length(G,mand_order[i], mand_order[i+1])

        cost += nx.dijkstra_path_length(G, mand_order[-1], arrival)

        tour_order[0]=0
        for i in range(len(mandatories)):
            tour_order[i + 1]= i + 2

        tour_order[len(mandatories)+1] = 1
        tour_order[len(mandatories)+2] = ngs
        tour_order[len(mandatories)+3] = 0
        upper_bound = cost
    print("\n upp %s"%upper_bound)
    print("\n cos %s"%tour_order)

    """
    NA = np.array([
    [0.0,  3.0 , 4.0 , 2.0 , 7.0],
    [3.0,  0.0 , 4.0 , 6.0 , 3.0],
    [4.0 , 4.0 , 0.0 , 5.0 , 8.0],
    [2.0  ,6.0 , 5.0 , 0.0 , 6.0],
    [7.0 , 3.0 , 8.0  ,6.0 , 0.0]])
    """
    start_time = time.time()
    solver.optimize(tour_order, NA, departure, arrival, inf, cuts_group, score_value, upper_bound, visits_group, root_visits_group)

    #CONVERT PATH
    compute_time = time.time() - start_time
    tour_order_int = tour_order.astype(int)
    solution_cost = inf[0]
    visits = int(inf[1])
    cuts = int(inf[2])
    mand_order_int = np.zeros(len(mandatories))
    if tour_order_int[2] == 1:
        tour_order_int = np.flip(tour_order_int)

    for i in range(0, len(mandatories)):
        mand_order_int[i] = new_nodes[tour_order_int[i+1]]


    #Path rebuilding
    path = []
    path.extend(nx.dijkstra_path(G, departure, mand_order_int[0]));
    for i in range(mand_order_int.size - 1):
    	sp = nx.dijkstra_path(G,mand_order_int[i], mand_order_int[i+1])
    	del(sp[0])
    	path.extend(sp)
    sp = nx.dijkstra_path(G, mand_order_int[-1], arrival)
    del(sp[0])
    path.extend(sp)

    #Output

    return [path, solution_cost, mand_order_int, visits, cuts, compute_time, cuts_group, visits_group, root_visits_group, score_value]
