file = open("../input/graph.txt", "r")
sl = file.readlines()
number_of_nodes = int(sl[0])

x_size = number_of_nodes * 3
y_size = number_of_nodes

A = np.zeros((number_of_nodes,number_of_nodes))
A = np.asmatrix(A)

for i in range(len(sl)):
	if i != 0:
	    st = sl[i]
	    st = st.split(",")
	    ind_i = int(st[0])
	    ind_j = int(st[1])
	    cost = float(st[2])
	    A[ind_i,ind_j]=cost
