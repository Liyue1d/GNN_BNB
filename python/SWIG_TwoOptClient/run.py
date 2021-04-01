#Loading Hyperparameters
exec(open("./../params/params.py").read())

#Raw data gen
exec(open("./data_gen.py").read())

#Data filtering
#exec(open("./trifinal.py").read())

#Data Shuffling, and training set and test set
exec(open("./shuffle.py").read())

#store graph data into pickle file
exec(open("./graph_to_pickle.py").read())
