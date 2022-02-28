from transformers import BertTokenizer
from modeling.character_bert import CharacterBertModel
from utils.character_cnn import CharacterIndexer
# from utils.character_cnn import CharacterMapper
import torch
from torch.nn.utils.rnn import pad_sequence
import numpy as np
input_x =[[[1],[2],[3]],[[4],[5],[6],[7],[8]],[[8],[9]]]
input_x2 = [[1,2,3,4,5,6,7]]
norm_data_pad = pad_sequence([torch.from_numpy(np.array(x)) for x in input_x2], batch_first=True)
j = 0
for i in range(len(input_x2[0])):

    if input_x2[0][i] == 7:
        break
    j = j + 1
print(j)
print(norm_data_pad)
