# GNN_BNB

Computes optimal solutions in a graph to problems instances I = (s,d,M) where: s is the start node, d the end node and M the list of mandatory nodes to visit at least once.

Uses a pre-trained graph neural network to first compute an upper bound, then leverages the upper bound for cuts in a branch & bound tree search which returns the optimal solution.

Requirements:
-SWIG (need to setup config files for numpy so C++ knows where to look for required files), numpy, networkx, scipy, tensorflow

Installation instructions: 

1) Install Cuda
Export to Path and Environment variables
See guide : https://docs.nvidia.com/cuda/archive/10.0/

2) Install Pip for python 3: sudo apt-get install python3-pip

3) Install tensorflow GPU: pip3 install tensorflow-gpu
If any problems, install older versions of tensorflow-gpu.
Tested successfully with tensorflow-gpu 1.4.0

3) Install cuDNN v7.6.2 (July 22, 2019), for CUDA 10.0(create Nvidia account):
https://developer.nvidia.com/rdp/cudnn-download
(Install Runtime, developer, code samples for Ubuntu version)

4) Install Numpy : pip3 install numpy

5) Install Scipy: sudo apt-get install python3-scip

6) Install Networkx: pip3 install networkx

7) Install SWIG: sudo apt-get install swig

8) Go to hybrid_2OPT_simu/hybrid_2OPT_simu/python/SWIG_TwoOptClient and edit swig_compile.sh:
- If needed, correct the following address to python3.5 package: /usr/include/python3.5/
- If needed, correct the following address to numpy: /usr/lib/python3/dist-packages/numpy/core/include/

9) Run sudo ./swig_compile.sh

Run swig_compile.sh once SWIG has been installed properly.

Place the desired graph in python/input, then run python/SWIG_TwoOptClient/graph_to_pickle.py to load the graph. 

Run python/SWIG_TwoOptClient/trainGCN.py to train the graph neural network on optimal data.

Model is then ready to be used on new examples with the python/SWIG_TwoOptClient/chain_single_example.py file.
