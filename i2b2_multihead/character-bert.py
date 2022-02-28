from transformers import BertTokenizer
from modeling.character_bert import CharacterBertModel
from utils.character_cnn import CharacterIndexer
# from utils.character_cnn import CharacterMapper
import  torch
from pytorch_transformers import *
from transformers import BertTokenizer
from modeling.character_bert import CharacterBertModel
from utils.character_cnn import CharacterIndexer
from torch.nn.utils.rnn import pad_sequence
# Example text
x = "Hello World! fdjaojfoadj fpadkfodaj"
x2 = "Hello World!"
# Tokenize the text
tokenizer = BertTokenizer.from_pretrained(
    './pretrained-models/bert-base-uncased/')
x = tokenizer.basic_tokenizer.tokenize(x)
x2 = tokenizer.basic_tokenizer.tokenize(x2)
# x = ['[CLS]', *x, '[SEP]','[PAD]','[PAD]','[PAD]']
# x2 = ['[CLS]']
x = 'this is a enample'.split()
x2 = 'why mot'.split()
print(x)
print(x2)

# tokens_id = torch.tensor(
#             tokenizer.convert_tokens_to_ids(x))
# tokens_id2 = torch.tensor(
#             tokenizer.convert_tokens_to_ids(x2))
# tokens_id = pad_sequence([tokens_id, tokens_id2], batch_first=True)
# print(tokens_id)
indexer = CharacterIndexer()
batch = [x, x2]
print(batch)

batch_ids1 = indexer.as_padded_tensor(batch)
pad_ids1 = indexer.as_padded_tensor([x2])
tokens = batch_ids1
# notpad = tokens[0] != pad_ids1 # no pad
# notcls = tokens != 257
# notsep = tokens != 261
# batch_ids2 = pad_sequence(batch_ids1, batch_first=True)
print(batch_ids1)
# batch_ids1 = torch.tensor(batch_ids1)
# print(batch_ids1)
# print('ddd',pad_ids1[0])
mask = batch_ids1 != indexer.as_padded_tensor([x2])[0][0]
print(mask)
# print(batch_ids1[0][0])
# print(pad_ids1[0,0])
# i = 0
# for t in batch_ids1[0]:
#
#     if torch.equal(t,pad_ids1[0,0]):
#         batch_ids1[0][i] = 0
#     i = i + 1
# a = torch.equal(batch_ids1[0,0], pad_ids1[0,0])
# print(a)
        # batch_ids1[:,:,t] = 0
# batch_ids1[:,0] = 0
# print(batch_ids1)
# print(pad_ids1)
# model = CharacterBertModel.from_pretrained(
#     './pretrained-models/medical_character_bert/')

# Feed batch to CharacterBERT & get the embeddings
# embeddings_for_batch = model(batch_ids1)
# embeddings_for_x = embeddings_for_batch[0]
# print(embeddings_for_batch.size())
# print('These are the embeddings produces by CharacterBERT (last transformer layer)')
# for token, embedding in zip(batch, embeddings_for_x):
#     print(token, embedding)
# embeddings_for_x = embeddings_for_batch[0]
# print(embeddings_for_x.size())
# batch_ids2 = indexer.as_padded_tensor(x)
# print(batch_ids2)
# print(batch_ids1.size())
# print(batch_ids2.size())
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
# model = CharacterBertModel.from_pretrained(
#     './pretrained-models/medical_character_bert/')
#
# text = "CharacterBERT attends to each tokens characters"
# tokenized_text = bert_tokenizer.basic_tokenizer.tokenize(text)
# tokenized_text = ['[CLS]'] + tokenized_text + ['[SEP]'] + ['[PAD]'] + ['[PAD]'] + ['[PAD]']
# print(tokenized_text)
#
# indexer = CharacterIndexer()  # This converts each token into a list of character indices
# input_tensor = indexer.as_padded_tensor([tokenized_text])
# print(input_tensor.size())
# print(input_tensor)
#
#
# text2 = ['[CLS]','CharacterBERT', 'attends', 'to', 'each', 'tokens','characters','[SEP]','[PAD]' ,'[PAD]' ,'[PAD]']
# tokenized_text2 = bert_tokenizer.tokenize(' '.join(text2))
# print(tokenized_text2)
# tokens_id = torch.tensor(
#                 bert_tokenizer.convert_tokens_to_ids(tokenized_text2))
# print(tokens_id.size())
# pad_seq = pad_sequence(tokens_id)
# print(pad_seq)