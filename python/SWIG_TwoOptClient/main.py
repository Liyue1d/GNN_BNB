import sys
sys.path.insert(0, 'src/')
from TwoOptClient import twoOptCompute
import numpy as np

A = np.zeros((23,23))
A = np.asmatrix(A)
file = open("GOMA_graph.txt", "r")
sl = file.readlines()
for i in range(len(sl)):
    st = sl[i]
    st = st.split(",")
    ind_i = int(st[0])
    ind_j = int(st[1])
    cost = float(st[2])
    A[ind_i,ind_j]=cost


instance = [18, 4, [1, 2, 3, 5, 10]]
results = twoOptCompute(A,instance)
path = results[0]
solution_cost = results[1]
mand_order_int = results[2]
attempts = results[3]
swap_cnt = results[4]
permutation_group = results[5]
compute_time = float(results[6])
score_value = results[7]

print("\nOrder of visit of mandatory nodes: %s"%mand_order_int)
print("Solution path : %s"%path)
print("Cost of solution path : %.2f "%solution_cost)
print("Number of attempted swaps : %d "%attempts)
print("Number of swaps : %d \n"%swap_cnt)
print("permutation_group : %s \n"%permutation_group)
print("compute time : %f \n"%compute_time)
print("score : %s \n"%score_value)
