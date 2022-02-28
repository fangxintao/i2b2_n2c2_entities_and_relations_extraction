import os
import json
import time
import argparse

import torch

from typing import Dict, List, Tuple, Set, Optional
from torch.utils.tensorboard import SummaryWriter
from prefetch_generator import BackgroundGenerator
from tqdm import tqdm

from torch.optim import Adam, SGD
from pytorch_transformers import AdamW, WarmupLinearSchedule
# from lib.preprocessings import Chinese_selection_preprocessing, Conll_selection_preprocessing, Conll_bert_preprocessing
from lib.preprocessings import i2b2_preprocessing, i2b2_bert_preprocessing
from lib.dataloaders import Selection_Dataset, Selection_loader
from lib.metrics import F1_triplet, F1_ner
from lib.models import MultiHeadSelection
from lib.config import Hyper
#import Concept_relation_preprocessing
#创建参数步骤
parser = argparse.ArgumentParser()
parser.add_argument('--exp_name',
                    '-e',
                    type=str,
                    default='conll_bert_re',
                    help='experiments/exp_name.json')
parser.add_argument('--mode',
                    '-m',
                    type=str,
                    default='preprocessing',
                    help='preprocessing|train|evaluation')
args = parser.parse_args()
#解析参数步骤

class Runner(object):
    def __init__(self, exp_name: str):
        self.exp_name = exp_name
        self.model_dir = 'saved_models/medical_bert_strict_lr_0.001_batch_size_32_dropout_0.1_5selection_loss'

        self.hyper = Hyper(os.path.join('experiments',
                                        self.exp_name + '.json'))

        self.gpu = self.hyper.gpu
        self.preprocessor = None
        self.triplet_metrics = F1_triplet()
        self.ner_metrics = F1_ner()
        self.optimizer = None
        self.model = None
        self.lr_schedule = None
        self.writer = SummaryWriter('./loss/medical_bert_strict_lr_0.001_batch_size_32_dropout_0.1_5selection_loss')
    def _optimizer(self, name, model):
        # mylist = list(map(id, model.tagger.parameters()))
        # base_params = filter(lambda p: id(p) not in mylist, model.parameters())
        m = {
            'adam': Adam(model.parameters()),
            'sgd': SGD(model.parameters(), lr=0.5),
            # 'adamw': AdamW([{'params': base_params}, {'params': model.tagger.parameters(), 'lr': 0.05}], lr=0.001)
            'adamw': AdamW(model.parameters(), lr=0.001)
        }
        return m[name]

    def _init_model(self):
        self.model = MultiHeadSelection(self.hyper).cuda(self.gpu)

    def preprocessing(self):
        # if self.exp_name == 'conll_selection_re':
        #     self.preprocessor = Conll_selection_preprocessing(self.hyper)
        # elif self.exp_name == 'chinese_selection_re':
        #     self.preprocessor = Chinese_selection_preprocessing(self.hyper)
        # elif self.exp_name == 'conll_bert_re':
        #     self.preprocessor = Conll_bert_preprocessing(self.hyper)
        if self.exp_name == 'i2b2_selection_re':
            self.preprocessor = i2b2_preprocessing(self.hyper)
        elif self.exp_name == 'i2b2_bert_re':
            self.preprocessor = i2b2_bert_preprocessing(self.hyper)
        self.preprocessor.gen_relation_vocab()
        self.preprocessor.gen_all_data()
        self.preprocessor.gen_vocab(min_freq=1)
        # for ner only
        self.preprocessor.gen_bio_vocab()

    def run(self, mode: str):
        if mode == 'preprocessing':
            self.preprocessing()
        elif mode == 'train':
            self._init_model()
            self.optimizer = self._optimizer(self.hyper.optimizer, self.model)
            # self.lr_schedule = WarmupLinearSchedule(self.optimizer, 50, 100)
            self.train()
        elif mode == 'evaluation':
            self._init_model()
            self.load_model(epoch=self.hyper.evaluation_epoch)
            self.evaluation(mode='evaluation', epoch=self.hyper.evaluation_epoch)
        else:
            raise ValueError('invalid mode')

    def load_model(self, epoch: int):
        self.model.load_state_dict(
            torch.load(
                os.path.join(self.model_dir,
                             self.exp_name + '_' + str(epoch))))

    def save_model(self, epoch: int):
        if not os.path.exists(self.model_dir):
            os.mkdir(self.model_dir)
        torch.save(
            self.model.state_dict(),
            os.path.join(self.model_dir, self.exp_name + '_' + str(epoch)))

    def evaluation(self, mode: str, epoch):
        if mode == 'train':
            dev_set = Selection_Dataset(self.hyper, self.hyper.dev)
            loader = Selection_loader(dev_set, batch_size=self.hyper.eval_batch, pin_memory=True)
        elif mode == 'evaluation':
            test_set = Selection_Dataset(self.hyper, self.hyper.test)
            loader = Selection_loader(test_set, batch_size=self.hyper.eval_batch, pin_memory=True)
        self.triplet_metrics.reset()
        self.model.eval()

        pbar = tqdm(enumerate(BackgroundGenerator(loader)), total=len(loader))

        with torch.no_grad():
            with open("i2b2_20211013.json", mode='w', encoding='utf-8') as ff:
                for batch_ndx, sample in pbar:
                    output = self.model(sample, is_train=False)
                    # dev_loss = output['dev_loss']
                    # dev_crf_loss = output['dev_crf_loss']
                    # dev_selection_loss = output['dev_selection_loss']
                    self.ner_metrics(output['gold_tags'], output['decoded_tag'])
                    self.triplet_metrics(output['selection_triplets'], output['spo_gold'])

                if mode == 'evaluation':
                    # Simple Contrastive Learning of Sentence Embeddings
                    for i, j, k, l, m in zip(output['gold_tags'], output['decoded_tag'],
                                             output['spo_gold'], output['selection_triplets'],
                                             output['text']):

                        for p in range(len(m)):
                            if m[p] == '[PAD]':
                                m = m[:p]
                                break
                        result = {
                            # 'text': ','.join(mm for mm in m),
                            'text': m,
                            'gold_tags': i,
                            'decoded_tag': j,
                            'spo_gold': k,
                            'selection_triplets': l,
                        }
                        ff.write(json.dumps(result))
                        ff.write('\n')
            triplet_result = self.triplet_metrics.get_metric()
            ner_result = self.ner_metrics.get_metric()
            # if mode == 'train':
            #     self.writer.add_scalars('i2b2', {'dev_loss': dev_loss}, global_step=epoch)  # 这里虽然test时也是用相同的代码，但我们只需可视化验证集上的loss就行
            #     self.writer.add_scalars('i2b2_inner', {'dev_crf_loss': dev_crf_loss}, global_step=epoch)
            #     self.writer.add_scalars('i2b2_inner', {'dev_selection_loss': dev_selection_loss}, global_step=epoch)
            #     self.writer.add_scalars('i2b2', {'F_score': triplet_result['fscore']}, global_step=epoch)
            # print(output['test_description'](
            #     epoch, self.hyper.epoch_num))
            pbar.set_description(output['dev_description'](
                epoch, self.hyper.epoch_num))

            print('Triplets-> ' + ', '.join([
                "%s: %.4f" % (name[0], value)
                for name, value in triplet_result.items() if not name.startswith("_")
            ]) + ' ||' + 'NER->' + ', '.join([
                "%s: %.4f" % (name[0], value)
                for name, value in ner_result.items() if not name.startswith("_")
            ]))



            for i in range(0, 8):
                triplet_result0 = self.triplet_metrics.get_metric0(i)
                print('（' + str(i) + '）Triplets-> ' + ', '.join([
                    "%s: %.4f" % (name[0], value)
                    for name, value in triplet_result0.items() if not name.startswith("_")
                ]))



    def train(self):
        train_set = Selection_Dataset(self.hyper, self.hyper.train)
        loader = Selection_loader(train_set, batch_size=self.hyper.train_batch, pin_memory=True)
        # dataloader 中shuffle(即是否重新洗牌)默认值为flase,其它默认值batch_size =1,pin_memory=flase
        # selection_loader其实就相当于固定了某些参数的data_loader
        for epoch in range(self.hyper.epoch_num):
            self.model.train()
            # 为啥要写上面这么一行
            pbar = tqdm(enumerate(BackgroundGenerator(loader)),
                        total=len(loader), disable=True)

            for batch_idx, sample in pbar:
                self.optimizer.zero_grad()
                output = self.model(sample, is_train=True)
                loss = output['loss']
                loss.backward()

                self.optimizer.step()
                # self.lr_schedule.step()

                pbar.set_description(output['description'](
                    epoch, self.hyper.epoch_num))
            loss = output['loss']
            crf_loss = output['crf_loss']
            selection_loss = output['selection_loss']
            self.writer.add_scalars('i2b2', {'train_loss': loss}, global_step=epoch)
            self.writer.add_scalars('i2b2_inner', {'crf_loss': crf_loss}, global_step=epoch)
            self.writer.add_scalars('i2b2_inner', {'selection_loss': selection_loss}, global_step=epoch)
            if epoch % self.hyper.print_epoch == 0 and epoch >= 3:
                self.save_model(epoch)
            print(epoch)
            pbar.set_description(output['description'](
                epoch, self.hyper.epoch_num))
            # if epoch % self.hyper.print_epoch == 0 and epoch >= 3:
            self.evaluation(mode='train', epoch=epoch)




if __name__ == "__main__":
    config = Runner(exp_name=args.exp_name)
    config.run(mode=args.mode)
    #print(torch.cuda.is_available())
    #config = Runner('conll_selection_re')
    #config.run('preprocessing')
    # config = Runner('i2b2_bert_re')
    # config.run('evaluation')

