#Takes raw data, shuffles it, and splits it into training set and test set

import h5py
import numpy as np
import random
import math

print("\n............Opening raw data............")
f_set = h5py.File("../model_utils/raw_data.hdf5", "r+")
d_set = f_set['raw']
length = d_set.shape[0]
width = d_set.shape[1]
shuffled_file = h5py.File("../model_utils/shuffled.hdf5", "w")
shuf = shuffled_file.create_dataset('shuffled', (length,width),
                        dtype='i')

print("\n............Shuffling raw data, this might take long............")
indices = []
for i in range(length):
    indices.append(i)

for i in range(length):
    print("\n %d / %d"%(i,length))
    r = random.randint(0,len(indices)-1)
    re = indices[r]
    shuf[re] = d_set[i]
    del(indices[r])
print("\n............Raw data shuffled............")

if length > 200000:
    test_l = 40000
else:
    test_l = math.floor(0.2 * length)

train_l = length - test_l

print("\n............Creating training set and test set............")

f_train_test = h5py.File("../model_utils/train_test.hdf5", "w")

d_train_set = f_train_test.create_dataset('training_set', (train_l,width),
                        dtype='i')
d_test_set = f_train_test.create_dataset('test_set', (test_l,width),
                        dtype='i')

d_train_set[0:train_l] = shuf[0:train_l]
d_test_set[0:test_l] = shuf[train_l:]


f_set.close()
f_train_test.close()
shuffled_file.close()

print("\n Training set and test set successfully created")
