import torch
import torch.nn as nn
import torch.nn.functional as F
from pytorch_transformers import BertForSequenceClassification, XLNetForSequenceClassification, RobertaForSequenceClassification, BertModel
import platform
from .MultiHeadSelfAttention import MultiHeadAttention

from torch.autograd import Function


torch.manual_seed(1234)
torch.cuda.manual_seed(1234)


class RNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.RNN(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        output, hidden = self.rnn(embedded)

        assert torch.equal(output[-1, :, :], hidden.squeeze(0))

        return self.fc(hidden.squeeze(0))


class LSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim,
                 n_layers=1, use_bidirectional=False, use_dropout=False):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim, num_layers=n_layers,
                           bidirectional=use_bidirectional,
                           dropout=0.5 if use_dropout else 0.)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        self.dropout = nn.Dropout(0.5 if use_dropout else 0.)

    def forward(self, x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.rnn(embedded)
        # seq len * batch * embedd
        # print(output.shape)
        # output = output.max(0)[0]
        # print(output.shape)

        hidden = self.dropout(torch.cat((hidden[-2, :, :], hidden[-1, :, :]),
                                        dim=1))

        return self.fc(hidden.squeeze(0))
        # return self.fc(self.dropout(output))


class CNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, n_filters, filter_sizes,
                 output_dim, use_dropout):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.convs = nn.ModuleList([
            nn.Conv2d(in_channels=1, out_channels=n_filters,
                      kernel_size=(fs, embedding_dim)) for fs in filter_sizes
        ])
        self.fc = nn.Linear(len(filter_sizes) * n_filters, output_dim)
        self.dropout = nn.Dropout(0.5 if use_dropout else 0.)

    def forward(self, x):
        x = x.permute(1, 0)
        embedded = self.embedding(x)
        embedded = embedded.unsqueeze(1)

        conved = [F.relu(conv(embedded)).squeeze(3) for conv in self.convs]
        pooled = [F.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]

        cat = self.dropout(torch.cat(pooled, dim=1))

        return self.fc(cat)


class LSTM_with_Attention(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim,
                 n_layers=1, use_bidirectional=False, use_dropout=False):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn = nn.LSTM(embedding_dim, hidden_dim // 2,
                           bidirectional=use_bidirectional,
                           dropout=0.5 if use_dropout else 0.)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.dropout = nn.Dropout(0.5 if use_dropout else 0.)

    def attention_net(self, lstm_output, final_state):
        lstm_output = lstm_output.permute(1, 0, 2)
        hidden = final_state.squeeze(0)
        attn_weights = torch.bmm(lstm_output, hidden.unsqueeze(2)).squeeze(2)
        soft_attn_weights = F.softmax(attn_weights, dim=1)
        new_hidden_state = torch.bmm(lstm_output.transpose(1, 2),
                                     soft_attn_weights.unsqueeze(2)).squeeze(2)

        return new_hidden_state

    def attention(self, lstm_output, final_state):
        lstm_output = lstm_output.permute(1, 0, 2)
        merged_state = torch.cat([s for s in final_state], 1)
        merged_state = merged_state.squeeze(0).unsqueeze(2)
        weights = torch.bmm(lstm_output, merged_state)
        weights = F.softmax(weights.squeeze(2), dim=1).unsqueeze(2)
        return torch.bmm(torch.transpose(lstm_output, 1, 2), weights).squeeze(2)

    def forward(self, x):
        embedded = self.embedding(x)
        output, (hidden, cell) = self.rnn(embedded)

        # attn_output = self.attention_net(output, hidden)
        attn_output = self.attention(output, hidden)

        return self.fc(attn_output.squeeze(0))


class CNN_LSTM(nn.Module):
    def __init__(self):
        pass

    def forward(self, x):
        pass


class Bertmodel(nn.Module):
    def __init__(self, args, in_dim=100, hidden_size=100, num_classes=3):
        super(Bertmodel, self).__init__()
        if platform.system() == 'Linux' or 'Darwin':
            self.bert = BertForSequenceClassification.from_pretrained(args.path + '/bert-base-uncased', num_labels=num_classes)
        else:
            self.bert = BertForSequenceClassification.from_pretrained(args.path + '\\bert-base-uncased',
                                                                      num_labels=num_classes)
        # self.bert = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
        # for param in self.bert.parameters():
        #     param.requires_grad = True
        # self.dropout = nn.Dropout(0.5)
        # self.fc = nn.Linear(self.hidden_size, self.num_classes)

    def forward(self, text):
        input_mask = text[:, 1, :].long()
        segment_ids = text[:, 2, :].long()
        input_ids = text[:, 0, :].long()
        output = self.bert(input_ids = input_ids, attention_mask = input_mask, token_type_ids = segment_ids)
        # output = self.dropout(output)
        return output[0]


class Bertcnnmodel(nn.Module):
    def __init__(self, args, in_dim=768, hidden_size=100, num_classes=3):
        super(Bertcnnmodel, self).__init__()
        if platform.system() == 'Linux' or 'Darwin':
            self.bert = BertModel.from_pretrained(args.path + '/bert-base-uncased', output_hidden_states=True)
        else:
            self.bert = BertModel.from_pretrained(args.path + '\\bert-base-uncased', output_hidden_states=True)
        self.conv = nn.Conv2d(1, 1, kernel_size=(3, 768), stride=1, padding=0)
        self.pool = nn.MaxPool1d(kernel_size=48, stride=1)
        self.linear1 = nn.Linear(13, 13)
        self.linear2 = nn.Linear(13, num_classes)
        # self.bert = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)
        # for param in self.bert.parameters():
        #     param.requires_grad = True
        # self.dropout = nn.Dropout(0.5)
        # self.fc = nn.Linear(self.hidden_size, self.num_classes)


    def forward(self, text):
        input_mask = text[:, 1, :].long()
        segment_ids = text[:, 2, :].long()
        input_ids = text[:, 0, :].long()
        output = self.bert(input_ids=input_ids, attention_mask=input_mask, token_type_ids=segment_ids)

        record = []
        for i in range(len(output[2])):
            max_val = self.conv(output[2][i].unsqueeze(1)).squeeze(1).max(dim=1)[0]
            record.append(max_val)

        x = torch.cat(tuple(record), dim=1)

        x = self.linear1(x).relu()
        x = self.linear1(x)
        x = self.linear2(x)
        # output = self.dropout(output)
        return x


class BertMultiTaskmodel(nn.Module):
    def __init__(self, args, in_dim=768, hidden_size=100, num_classes=3, dom_classes=32, num_heads=2):
        super(BertMultiTaskmodel, self).__init__()
        if platform.system() == 'Linux' or 'Darwin':
            self.bert = BertModel.from_pretrained(args.path + '/bert-base-uncased', output_hidden_states=True)
        else:
            self.bert = BertModel.from_pretrained(args.path + '\\bert-base-uncased', output_hidden_states=True)
        self.conv = nn.Conv2d(1, 1, kernel_size=(3, in_dim), stride=1, padding=0)  # for sentence
        self.conv2 = nn.Conv2d(1, 1, kernel_size=(3, in_dim), stride=1, padding=0)  # for domain
        self.pool = nn.MaxPool1d(kernel_size=4, stride=1)  # for sentence
        self.pool2 = nn.MaxPool1d(kernel_size=4, stride=1)  # for domain
        self.attn = MultiHeadAttention(10, num_heads)  # for sentence
        self.attn2 = MultiHeadAttention(10, num_heads)  # for domain
        self.linear1 = nn.Linear(23, 10)
        self.linear2 = nn.Linear(10, num_classes)  # Sentiment classifier
        self.linear3 = nn.Linear(46, 10)
        self.linear4 = nn.Linear(10, dom_classes)  # Domain classifier
        # self.rnn = nn.LSTM(in_dim, hidden_size, num_layers=3,
        #                    bidirectional=True,
        #                    dropout=0.5)
        # self.fc = nn.Linear(hidden_size * 2, dom_classes)
        self.Grl = GRL()


    def forward(self, text, domains, dom_lab):
        input_mask = text[:, 1, :].long()
        segment_ids = text[:, 2, :].long()
        input_ids = text[:, 0, :].long()
        output = self.bert(input_ids=input_ids, attention_mask=input_mask, token_type_ids=segment_ids)

        input_mask_dom = domains[:, 1, :].long()
        segment_ids_dom = domains[:, 2, :].long()
        input_ids_dom = domains[:, 0, :].long()
        output_dom = self.bert(input_ids=input_ids_dom, attention_mask=input_mask_dom, token_type_ids=segment_ids_dom)

        record = []
        for i in range(len(output[2])):
            max_val = self.conv(output[2][i].unsqueeze(1)).squeeze(1).max(dim=1)[0]
            record.append(max_val)

        x = torch.cat(tuple(record), dim=1)



        record_dom = []
        for i in range(len(output_dom[2])):
            max_val_dom = self.conv(output_dom[2][i].unsqueeze(1)).squeeze(1).max(dim=1)[0]
            record_dom.append(max_val_dom)

        x_dom = torch.cat(tuple(record_dom), dim=1)
        # 8*13
        x_pool = self.pool(x.unsqueeze(0)).squeeze()
        x_pool_dom = self.pool2(x_dom.unsqueeze(0)).squeeze()
        # 8*10
        # x = self.attn(torch.cat([x, x_pool], 1))
        # x_dom = self.attn2(torch.cat([x_dom, x_pool_dom], 1))
        x = torch.cat([x, x_pool_dom], 1)
        x_dom = torch.cat([x_dom, x_pool], 1)

        l_dom = self.linear1(x).relu()
        l_dom = self.Grl(l_dom)
        l_dom = self.linear4(l_dom)
        # output = self.dropout(output)

        l = self.linear3(torch.cat([x, x_dom], 1)).relu()
        l = self.linear2(l)

        return l, l_dom


class grl_func(torch.autograd.Function):
    def __init__(self):
        super(grl_func, self).__init__()

    @ staticmethod
    def forward(ctx, x, lambda_):
        ctx.save_for_backward(lambda_)
        return x.view_as(x)

    @ staticmethod
    def backward(ctx, grad_output):
        lambda_, = ctx.saved_variables
        grad_input = grad_output.clone()
        return - lambda_ * grad_input, None


class GRL(nn.Module):
    def __init__(self, lambda_=0.):
        super(GRL, self).__init__()
        self.lambda_ = torch.tensor(lambda_)

    def set_lambda(self, lambda_):
        self.lambda_ = torch.tensor(lambda_)

    def forward(self, x):
        return grl_func.apply(x, self.lambda_)