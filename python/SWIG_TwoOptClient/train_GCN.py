#Use of Thomas Kipf's kernel (2016)
#Optimized with the use of CudNN  v7 for the Tesla V100 GPUs in the DGX-station - use of CudNN v6 will cause loss of performance
#Requires python3 for average_gradients function
#Updated on 20/02/2018

import tensorflow as tf
import numpy as np
import pickle
import sys
import h5py
import os


os.environ["CUDA_VISIBLE_DEVICES"]="0"

# Hyperparameters
exec(open("./../model_params/params.py").read())

# Graph definition
exec(open("./defineGraph.py").read())
sess = tf.InteractiveSession(config=tf.ConfigProto(log_device_placement=True, allow_soft_placement=True))

sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()

#separation index between x and y
separationInd = number_of_features_per_node * number_of_nodes

#Load data

f = h5py.File("../model_utils/train_test.hdf5", "r")
trainSet = f['training_set']

testSet = f['test_set']
xTest = testSet[:,0:separationInd]
yTest = testSet[:,separationInd:]

#initilialize counters
#number of batch update
i = 0
#number of periods
periods = 0
#last cycle test set result improved
last_test_improvement = 0
#best_score_on_test
best_test_score = sys.float_info.max
#current index on the dataset
ind = 0
#length of training set
train_length = trainSet.shape[0]
#param : batch quarters
batch_quarter = batch_size/4
batch_quarter1 = 1 * batch_quarter
batch_quarter2 = 2 * batch_quarter
batch_quarter3 = 3 * batch_quarter
batch_quarter4 = 4 * batch_quarter

#Training the model

while last_test_improvement < early_stop:

    lower_batch_bound = ind
    upper_batch_bound = ind + batch_size

#if index points to end of training set
    if upper_batch_bound >= train_length:
        current_batch = trainSet[lower_batch_bound:]
        xSet = current_batch[:,0:separationInd]
        ySet = current_batch[:,separationInd:]
        sess.run(train_step_single, feed_dict = {x0: xSet, y0: ySet,
        dropout_prob: drop_probability, is_training: True})

#else
    else:
        current_batch = trainSet[lower_batch_bound:upper_batch_bound]
        xSet = current_batch[:,0:separationInd]
        ySet = current_batch[:,separationInd:]

        '''
        xSet0 = xSet[0:batch_quarter1]
        ySet0 = ySet[0:batch_quarter1]
        xSet1 = xSet[batch_quarter1:batch_quarter2]
        ySet1 = ySet[batch_quarter1:batch_quarter2]
        xSet2 = xSet[batch_quarter2:batch_quarter3]
        ySet2 = ySet[batch_quarter2:batch_quarter3]
        xSet3 = xSet[batch_quarter3:batch_quarter4]
        ySet3 = ySet[batch_quarter3:batch_quarter4]
        '''
        sess.run(train_step_single, feed_dict = {x0: xSet, y0: ySet,
        dropout_prob: drop_probability, is_training: True})
    if i % 100 == 0:
        train_batch_avg_loss, train_accuracy, train_summary = sess.run([average_loss0, accuracy, merged], feed_dict={
            x0: xSet, y0: ySet, dropout_prob: 1.0, is_training: False})

        test_avg_loss, test_accuracy, test_summary = sess.run([average_loss0, accuracy, merged], feed_dict={
            x0: xTest, y0: yTest, dropout_prob: 1.0, is_training: False})

        train_writer.add_summary(train_summary, i)
        test_writer.add_summary(test_summary, i)

        if test_avg_loss < best_test_score:
            best_test_score = test_avg_loss
            save_path = saver.save(sess, "../save/tuned_graph_net.ckpt")
            print("Model saved in path: %s" % save_path)

        else:
            last_test_improvement = last_test_improvement + 1


        print('step %d, training accuracy %g' % (i, train_accuracy))
        print('step %d, training batch avg loss %f' % (i, train_batch_avg_loss))
        print('step %d, test set accuracy %g' % (i, test_accuracy))
        print('step %d, test set batch avg loss %f' % (i, test_avg_loss))

    #update counters
    i += 1
    if upper_batch_bound >= train_length:
        ind = 0
        periods += 1
    else:
        ind = ind + batch_size


saver.restore(sess, "../save/tuned_graph_net.ckpt")
test_loss = sess.run(average_loss0, feed_dict={
    x0: xTest, y0: yTest, dropout_prob: 1.0, is_training: False})

file = open("../results/results.txt","w")
file.write("Results of model")
file.write("\nLayers : %s"%graph_layers)
file.write("\nBest value saved %f"%best_test_score)
file.write("\nRestored model avg loss : %f"%test_loss)
file.close()
