# GNN_BNB

Aims to compute optimal solutions in a graph to problems instances I = (s,d,M) where: s is the start node, d the end node and M the list of mandatory nodes to visit at least once.

Uses an Graph neural network to first compute an upper bound, then leverages the upper bound for cuts in a branch & bound tree search which returns the optimal solution.

Requirements:
-SWIG (need to setup config files for numpy so C++ knows where to look for required files), numpy, networkx, scipy, tensorflow

Instructions: Run swig_compile.sh once SWIG has been installed properly. Place the desired graph in python/input, then run python/SWIG_TwoOptClient/graph_to_pickle.py to load the graph. Next, run python/SWIG_TwoOptClient/trainGCN.py to train the graph neural network on optimal data. Model is then ready to be used on new examples with the python/SWIG_TwoOptClient/chain_single_example.py file.
