import pandas as pd
import torch
import argparse
from .model import Bertmodel, Bertcnnmodel
import os
from .extract_feature import bert_feature
from .dataloader import Loader
from torch.utils.data import Dataset, DataLoader
import time
import platform


torch.manual_seed(1234)
torch.cuda.manual_seed(1234)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def parse_args():
    parser = argparse.ArgumentParser(description="bert inference", add_help=False)
    parser.add_argument('--model_type', type=str, choices=['bert', 'bert_cnn'], required=True, help="Type of saved model")
    parser.add_argument('--model', type=str, required=True, help="Path to saved model")
    parser.add_argument('--path', type=str, default=os.getcwd(), help="pretrained bert model root path")
    parser.add_argument('--max_seq_length', type=int, default=50,
                        help='length')
    return parser.parse_args()


def main(args, raw_text):
    device = torch.device('cuda' if torch.cuda.is_available() and args.cuda else 'cpu')
    batch_size = 8
    # raw_text = ["I really like The Avengers cause it make me excited.",
    #             "LOL sucks!!!",
    #             "trades are welcome! DM if interested~",
    #             "Little gifts for lovely SG Carats! My 1st time preparing fansupport please enjoy ~",
    #             "I am at LAX international to pick my parents up and some k pop group just landed and people are going apeshit, I asked around they’re called Super Junior",
    #             "Someone said, I deserve to be filled the same way I pour and I felt that.",
    #             "His lil pout and the way he touched boss's neck!?!?? SCREAMING",
    #             "Russia says that it is relocating 500 Ukrainian children each day from Kherson to Russian territory. A harrowing admission of war crimes.",
    #             ]
    if args.model_type == 'bert':
        model = Bertmodel(args).to(device)
    else:
        model = Bertcnnmodel(args).to(device)
    model.load_state_dict(torch.load(args.model, map_location=device))

    time_start = time.time()

    test_df = pd.DataFrame({"data": raw_text, "target": ["Positive"]*len(raw_text)})
    sample = bert_feature(args, test_df)
    data = []
    for i in range(len(sample['target'])):
        temp = {}
        for key in sample.keys():
            temp[key] = sample[key][i]
        data.append(temp)
    datasets = {'infer': Loader(data, sequence_len=100, features_dim=100)}
    dataloaders = {
        ds: DataLoader(datasets[ds],
                       batch_size=batch_size,)
        for ds in datasets.keys()
    }

    preds = infer(model, dataloaders['infer'], batch_size)
    rounded_preds = [pred.max(1)[1] for pred in preds]

    time_end = time.time()

    label_map = {0: "Negative", 1: "Neutral", 2: "Positive"}
    res = []
    for i, text in enumerate(raw_text):
        batch_idx = i // batch_size
        sentence_idx = i % batch_size
        # print(text, label_map[rounded_preds[batch_idx][sentence_idx].item()])
        res.append(label_map[rounded_preds[batch_idx][sentence_idx].item()])
    print('time cost', time_end - time_start, 's')
    return res


def infer(model, iterator, batch_size):
    model.eval()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    res = []
    for batch in iterator:
        feature = batch['features'].to(device)
        preds = model(feature)
        while preds.shape[0] < batch_size:
            preds = torch.cat((preds, preds[0].unsqueeze(0)), 0)
        res.append(preds)

    return torch.stack(res)


class MyArgs:
    def __init__(self, model_type, model, path, max_seq_length):
        self.model_type = model_type
        self.model = model
        self.path = path
        self.max_seq_length = max_seq_length


# def parse_args_default():
#     parser = argparse.ArgumentParser(description="bert inference", add_help=False)
#     parser.add_argument('--model_type', type=str, default="bert_cnn", help="Type of saved model")
#     parser.add_argument('--model', type=str, default="./checkpoints/bert_cnn_adam_bs64_acc0.954.pth", help="Path to saved model")
#     parser.add_argument('--path', type=str, default=os.getcwd(), help="pretrained bert model root path")
#     parser.add_argument('--max_seq_length', type=int, default=50,
#                         help='length')
#     return parser.parse_args()

def get_prediction(raw_text: list) -> list:
    if platform.system() == 'Linux':
        args = MyArgs(model_type="bert_cnn", model="./SentimentModel/checkpoints/bert_cnn_adam_bs64_acc0.954.pth",
                      path="./SentimentModel", max_seq_length=50)
    elif platform.system() == 'Darwin':
        args = MyArgs(model_type="bert_cnn", model="./SentimentModel/checkpoints/bert_cnn_adam_bs64_acc0.954.pth",
                      path="./SentimentModel", max_seq_length=50)
    elif platform.system() == 'Windows':
        args = MyArgs(model_type="bert_cnn", model="TextEmotion\SentimentModel\checkpoints\\bert_cnn_adam_bs64_acc0.954.pth",
                      path="TextEmotion\SentimentModel", max_seq_length=50)
    predictions = main(args, raw_text)
    return predictions


if __name__ == '__main__':
    # args = parse_args()
    # print(args)
    # print(main(args, ["I really like The Avengers cause it make me excited.",
    #             "LOL sucks!!!",
    #             "trades are welcome! DM if interested~",
    #             "Little gifts for lovely SG Carats! My 1st time preparing fansupport please enjoy ~",
    #             "I am at LAX international to pick my parents up and some k pop group just landed and people are going apeshit, I asked around they’re called Super Junior",
    #             "Someone said, I deserve to be filled the same way I pour and I felt that.",
    #             "His lil pout and the way he touched boss's neck!?!?? SCREAMING",
    #             "Russia says that it is relocating 500 Ukrainian children each day from Kherson to Russian territory. A harrowing admission of war crimes.",
    #             ]))
    print(get_prediction(["I really like The Avengers cause it make me excited.",
                          "LOL sucks!!!",
                          "trades are welcome! DM if interested~",
                          ]))