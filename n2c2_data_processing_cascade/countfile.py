import glob
import os
import re
from typing import *
testpath = 'test'
trainpath = 'training_20180910'

# data_dev = 'data_new_0622/dev'
# data_test = 'data_new_0622/test'
# data_train = 'data_new_0622/train'
data_dev = 'data_new_0622/dev'
data_test = 'data_new_0622/test'
data_train = 'data_new_0622/train'

#
filenamelist = [os.path.basename(x) for x in glob.iglob(trainpath + '/*txt')]
# filenamelist1 = [os.path.basename(x) for x in glob.iglob(trainpath + '/*ann')]
filenamelist2 = [os.path.basename(x) for x in glob.iglob(testpath + '/*txt')]
# filenamelist3 = [os.path.basename(x) for x in glob.iglob(testpath + '/*ann')]

# filenamelist4 = [os.path.basename(x) for x in glob.iglob(data_dev + '/*ann')]
filenamelist5 = [os.path.basename(x) for x in glob.iglob(data_dev + '/*txt')]
# filenamelist6 = [os.path.basename(x) for x in glob.iglob(data_test + '/*ann')]
filenamelist7 = [os.path.basename(x) for x in glob.iglob(data_test + '/*txt')]
filenamelist8 = [os.path.basename(x) for x in glob.iglob(data_train + '/*txt')]


# linecount = 0
# for filename in filenamelist7:
#     f = open(h + "/" + filename, 'r')
#     lines = f.readlines()
#     for line in range(0,len(lines)):
#         linecount += 1
#

print(int(len(filenamelist)))
print(int(len(filenamelist2)))
print(int(len(filenamelist5)))
# print(int(len(filenamelist6)))
print(int(len(filenamelist7)))
print(int(len(filenamelist8)))