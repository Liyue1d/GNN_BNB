import sys
sys.path.insert(0, 'src/')
from TwoOptClient import twoOptCompute
import numpy as np

exec(open("./../input/graph.py").read())

exec(open("./pi.py").read())

instance = [1, 10, [7,8,11]]
nv = instance.copy()
nv[2] = instance[2].copy()
gcn_order = pi(nv)
order_inst = instance.copy()
order_inst[2] = gcn_order.copy()

#without init
results = twoOptCompute(A,instance,-1)

path = results[0]
solution_cost = results[1]
mand_order_int = results[2]
visits = results[3]
cuts = results[4]
compute_time = float(results[5])
cuts_group = results[6]
visits_group = results[7]

#with init
order_results = twoOptCompute(A,order_inst,1)
order_path = order_results[0]
order_solution_cost = order_results[1]
order_mand_order_int = order_results[2]
order_visits = order_results[3]
order_cuts = order_results[4]
order_compute_time = float(order_results[5])
order_cuts_group = order_results[6]
order_visits_group = order_results[7]

print("\nOrder suggested by GCN: %s"%gcn_order)

print("\nOrder of visit of mandatory nodes without init: %s"%mand_order_int)
print("Order of visit of mandatory nodes with init: %s"%order_mand_order_int)

print("\nSolution path without init: %s"%path)
print("Solution path with init: %s"%order_path)

print("\nCost of solution path without init: %.2f "%solution_cost)
print("Cost of solution path with init: %.2f "%order_solution_cost)

print("\nNumber of visits without init: %d "%visits)
print("Number of visits with init: %d "%order_visits)

print("\nNumber of cuts without init: %d \n"%cuts)
print("Number of cuts with init: %d \n"%order_cuts)

print("\ncompute time without init: %f \n"%compute_time)
print("compute time with init: %f \n"%order_compute_time)
