import os

import torch
from torchtext.data import Field, LabelField, TabularDataset, Iterator
from torchtext.vocab import Vectors
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM


torch.manual_seed(1234)
torch.cuda.manual_seed(1234)


class MyDataset(object):

    def __init__(self, root_dir='twitter_data', batch_size=64, use_vector=True, pdevice = 'cpu'):
        self.TEXT = Field(sequential=True, use_vocab=True, tokenizer_language='en_core_web_sm',
                          tokenize='spacy', lower=True, batch_first=True)
        self.LABEL = LabelField(dtype=torch.float)
        vectors = Vectors(name='mr_vocab.txt', cache='./')
        dataset_path = os.path.join(root_dir, '{}.tsv')

        # # pretrained bert
        # tokenizer = BertTokenizer.from_pretrained('bert_base_uncased/')  # 改为自己存放模型的目录
        # model = BertModel.from_pretrained('bert_base_uncased/')
        #
        # text = " the man went to the store "
        # tokenized_text = tokenizer.tokenize(text)  # token初始化
        # indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)  # 获取词汇表索引
        # tokens_tensor = torch.tensor([indexed_tokens])  # 将输入转化为torch的tensor
        # with torch.no_grad():  # 禁用梯度计算 因为只是前向传播获取隐藏层状态，所以不需要计算梯度
        #     last_hidden_states = model(tokens_tensor)[0]
        # token_embeddings = []
        #
        # for token_i in range(len(tokenized_text)):
        #     hidden_layers = []
        #     for layer_i in range(len(last_hidden_states)):
        #         vec = last_hidden_states[layer_i][0][token_i]  # 如果输入是单句不分块中间是0，因为只有一个维度，如果分块还要再遍历一次
        #         hidden_layers.append(vec)
        #     token_embeddings.append(hidden_layers)
        # concatenated_last_4_layers = [torch.cat((layer[-1], layer[-2], layer[-3], layer[-4]), 0) for layer in
        #                               token_embeddings]  # 连接最后四层 [number_of_tokens, 3072]
        # summed_last_4_layers = [torch.sum(torch.stack(layer)[-4:], 0) for layer in
        #                         token_embeddings]  # 对最后四层求和 [number_of_tokens, 768]
        # # b = torch.Tensor(len(summed_last_4_layers), summed_last_4_layers[0].shape[0], 1)
        # x = torch.stack(summed_last_4_layers)
        self.dataset = {}
        self.dataloader = {}
        for target in ['train', 'dev', 'test']:
            self.dataset[target] = TabularDataset(
                path=dataset_path.format(target),
                format='tsv',
                fields=[('text', self.TEXT), ('label', self.LABEL)]
            )
            if use_vector:
                self.TEXT.build_vocab(self.dataset[target], max_size=25000, vectors=vectors)
            else:
                self.TEXT.build_vocab(self.dataset[target], max_size=25000)

            self.LABEL.build_vocab(self.dataset[target])
            self.dataloader[target] = Iterator(self.dataset[target],
                                               batch_size=batch_size,
                                               device=pdevice,
                                               repeat=False,
                                               sort_key=lambda x: len(x.text),
                                               shuffle=True)


if __name__ == '__main__':
    dataset = MyDataset()
