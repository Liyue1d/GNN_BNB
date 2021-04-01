import pickle
import numpy as np
from numpy import linalg as LA
from scipy.linalg import fractional_matrix_power


def node_degree(x):
    #Returns the node degree matrix corresponding
    # to the input adjacency matrix x
    # Input: x is a numpy matrix
    # Output: nd_x is a numpy matrix
    size = x.shape[0]
    nd_x = np.matrix(np.zeros((size,size)))
    for i in range(size):
        nd_x[i,i] = np.sum(x[i])
    return nd_x


#Adjacency matrix definition
exec(open("./../input/graph.py").read())
adj_matrix = A
print("adj =  \n", adj_matrix)

#Number of nodes is stored into variable m_size
m_size = adj_matrix.shape[0]

a_chap = adj_matrix + np.eye(m_size)
print("achap = \n", a_chap)

d_chap = node_degree(a_chap)
print("dchap \n", d_chap)

inv_sq_root_d_chap = np.matrix(fractional_matrix_power(d_chap, -0.5))
print("inv_sq_root_d_chap =  \n", inv_sq_root_d_chap)
print("(inv_sq_root_d_chap*inv_sq_root_d_chap)^-1 =  \n", LA.inv(inv_sq_root_d_chap*inv_sq_root_d_chap))

sym_norm = inv_sq_root_d_chap * a_chap * inv_sq_root_d_chap
print("sym_norm =  \n", sym_norm)

data = {'adj': adj_matrix, 'prod_matrix': sym_norm, 'number_of_nodes':m_size}

#Write the data into a pickle file
with open('../model_utils/data.pickle', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
