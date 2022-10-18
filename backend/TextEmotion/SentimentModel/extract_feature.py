from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
import numpy as np
from pytorch_transformers import BertConfig
import pandas as pd
import os
import argparse
import pickle
import platform


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_seq_length', type=int, default = 50,
                        help='length')
    # parser.add_argument('--split_path', type=str, default = "/processed/split_data.json",
    #                     help='length')
    parser.add_argument('--save_path', type=str, default = "./twitter_data/bert_features",
                        help='length')
    return parser.parse_args()


def bert_feature(args, data):
    path = args.path
    # data_path = os.path.join(path, "annotation/" + language + "/labeled/total.json")
    # save_path = os.path.join(path, "annotation/" + language + args.split_path)
    if platform.system() == 'Linux' or 'Darwin':
        tokenizer = BertTokenizer.from_pretrained(path + '/bert-base-uncased', do_lower_case=True)
    else:
        tokenizer = BertTokenizer.from_pretrained(path + '\\bert-base-uncased', do_lower_case=True)

    # with open(data_path,'r',encoding='utf8') as fp:
    #     data = json.load(fp)

    max_seq_length = args.max_seq_length
    features = {}
    Input_ids, Input_mask, Segment_ids = [], [], []
    ids, users, Label = [], [], []
    harm, target, activation, polarity = [], [], [], []
    ment, tag = [], []
    raw_data = []
    max_len = 0

    for index, tweet in data.iterrows():
        # tweet_contant, hash_tag, mention = remove_tag(tweet['data'], remain=False)
        # tweet_contant, _ = do_clean(tweet_contant)
        tokens_a = tokenizer.tokenize(tweet['data'])
        if tweet['target'] == 'Negative':
            tweet['harm'] = '0'
        elif tweet['target'] == 'Neutral':
            tweet['harm'] = '1'
        elif tweet['target'] == 'Positive':
            tweet['harm'] = '2'

        if len(tokens_a) > max_seq_length - 2:
            tokens_a = tokens_a[:max_seq_length - 2]

        tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
        segment_ids = [0] * len(tokens)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        if len(input_ids) > max_len:
            max_len = len(input_ids)

        input_mask = [1] * len(input_ids)

        padding = [0] * (max_seq_length - len(input_ids))

        input_ids += padding
        input_mask += padding
        segment_ids += padding

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length

        Input_ids.append(input_ids)
        Input_mask.append(input_mask)
        Segment_ids.append(segment_ids)
        raw_data.append(tweet['data'])
        # ids.append(tweet['id'])
        # users.append(tweet['user'])
        harm.append(tweet['harm'])
        target.append(tweet['target'])
        # activation.append(tweet['activation'])
        # polarity.append(tweet['polarity'])
        # ment.append(mention)
        # tag.append(hash_tag)

        continue

    features['raw_data'] = np.array(raw_data)
    features['harm'] = np.array(harm)
    features['target'] = np.array(target)
    # features['activation'] = np.array(activation)
    # features['polarity'] = np.array(polarity)
    # features['id'] = np.array(ids)
    # features['user'] = np.array(users)
    Input_ids = np.expand_dims(Input_ids, 1)
    Input_mask = np.expand_dims(Input_mask, 1)
    Segment_ids = np.expand_dims(Segment_ids, 1)
    features['text'] = np.concatenate((Input_ids, Input_mask, Segment_ids), axis=1)

    return features


def save_data(args, features, file):
    path = os.getcwd()
    with open(os.path.join(path, args.save_path + '/' + file +'.pkl'),'wb') as file_obj:
        pickle.dump(features,file_obj)
        print('Save Successful!')


if __name__ == "__main__":
    args = parse_args()
    print(args)
    for file in ['train', 'dev', 'test']:
        df = pd.read_csv("twitter_data/"+file+".tsv", sep="\t", header=None)
        df.columns = ['data', 'target']
        data = df
        bert_Feature = bert_feature(args, data)
        save_data(args, bert_Feature, file)
