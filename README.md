# GNN_BNB

Aims to compute optimal solutions in a graph to problems instances I = (s,d,M) where: s is the start node, d the end node and M the list of mandatory nodes to visit at least once.

Uses an Graph neural network to first compute an upper bound, then leverages the upper bound for cuts in a branch & bound tree search which returns the optimal solution.

Requirements:
-SWIG (need to setup config files for numpy so C++ knows where to look for required files)
-numpy
-networkx
-scipy
-tensorflow
