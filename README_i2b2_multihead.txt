In this project, we apply the multi-head selection model to clinical data i2b2

Requirements:
Python 3.8
Transformers 3.3.1
Pytorch-transformers 1.0.0
Pytorch-crf 0.7.2
Torch 1.4.0
Tqdm 4.61.0

Usage:
一.Build train, dev, test data from n2c2 dataset by :

a) 
Switch to the corresponding directory

././i2b2_data_processing

b) 
firstly run:
	data_divide.py, 
	(I have put the dataset under the same path)
    (in this part, we random split the original data into train data, dev data and test data)
keep the output files and run:
	i2b2_preprocess.py
You will get three .txt file stored in ../raw_data/i2b2_256_85_85_cased_reassign
（Note that the path of the data should be aligned）

二. after got the three .txt files (train.txt, dev.txt, test.txt)

a) move the three .txt files to ././i2b2_multihead/raw_data/i2b2_256_85_85_cased
(I have put three files in there)

b) run as:
python main.py --mode preprocessing --exp_name i2b2_bert_re
python main.py --mode train --exp_name i2b2_bert_re 

After training, run:
python main.py --mode evaluation --exp_name i2b2_bert_re
to evaluate the effective of the model

