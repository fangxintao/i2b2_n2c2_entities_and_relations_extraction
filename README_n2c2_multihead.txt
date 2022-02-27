In this project, we apply the multi-head selection model to clinical data n2c2

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

././n2c2_data_processing_multihead

b) 
firstly run:
	data_divide.py, 
	(I have put the dataset under the same path)
then run:
	preprocess.py
You will get three .txt file
（Note that the path of the data should be aligned）

二. after got the three .txt files (train.txt, dev.txt, test.txt)

a) move the three .txt files to ././n2c2_multihead/raw_data/n2c2_data_version3 
(I have put three files in there)

b) run as:
python main.py --mode preprocessing --exp_name n2c2_bert_re
python main.py --mode train --exp_name n2c2_bert_re 

After training, run:
python main.py --mode evaluation --exp_name n2c2_bert_re
to evaluate the effective of the model

三.Noted
We built several different models and  We store each model in a different file and place it in the same folder
././n2c2_multihead/lib/models/

You should change some codes in main.py if you want to utilize those models

There is a function called _init_model(), and if you want to utilize other model, 
Please assign the class name of the corresponding model to the self.model in _init_model()


Please download the pre-trained language model to be used in the model in advance. The reference URL is as follows:

https://github.com/helboukkouri/character-bert.

The last, the way of using Character-BERT needs to modify some code, we wrote a part in the comments, but please find the specific use method by yourself
Please download the pre-trained language model to be used in the model in advance. The reference URL is as follows:

https://github.com/helboukkouri/character-bert.

The last, the way of using Character-BERT needs to modify some code, we wrote a part in the comments, but please refer to the webpage just now for the specific use method