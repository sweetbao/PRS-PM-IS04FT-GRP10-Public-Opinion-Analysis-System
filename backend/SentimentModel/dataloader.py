import os
import sys
import json
import nltk
from tqdm import tqdm


import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler, SequentialSampler
import pickle


class Loader(Dataset):
    def __init__(self, df, sequence_len, features_dim):
        self.df = df
        self.sequence_len = sequence_len
        self.features_dim = features_dim

    def __len__(self):
        return len(self.df)

    def __getitem__(self, item):
        # user = self.df[item]['user']
        # ids = self.df[item]['id']
        res = torch.Tensor(self.df[item]['text'])
        label = int(self.df[item]['harm'])
        sample = {
            'features': res,
            'labels': label,
            # 'id': ids,
            # 'user': user
        }
        return sample


def BertDataLoader( index=None, mask=None, sequence_len=100, features_dim=100, batch_size=8, num_workers=8,
                   shuffle=False, debug_mode=False, size='normal'):
    # data_path = args.data_path
    set_name = ["train", "dev", "test"]
    train_df, valid_df, test_df = [None, None, None]
    for name in set_name:
        data_path = 'twitter_data/bert_features/'+name+'.pkl'
        # data_path = 'twitter_data/bert_features/' + 'test' + '.pkl'
        with open(data_path, 'rb') as fp:
            pkldata = pickle.load(fp)

        data = []

        for i in range(len(pkldata['target'])):
            temp = {}
            for key in pkldata.keys():
                temp[key] = pkldata[key][i]
            data.append(temp)
        if name == "train":
            train_df = data
        elif name == "dev":
            valid_df = data
        elif name == "test":
            test_df = data

    datasets = {
        'train': Loader(train_df, sequence_len, features_dim),
        'valid': Loader(valid_df, sequence_len, features_dim),
        'test': Loader(test_df, sequence_len, features_dim),
    }

    dataloaders = {
        ds: DataLoader(datasets[ds],
                       batch_size=batch_size,
                       num_workers=num_workers,)
        for ds in datasets.keys()
    }
    return dataloaders


if __name__ == '__main__':
    data = BertDataLoader()
    print(data)


